import csv
import os
import os.path as op
import time
from collections import OrderedDict
import datetime
import subprocess
from AndroidRunner import util
from AndroidRunner import Adb
from AndroidRunner.Plugins.Profiler import Profiler
from AndroidRunner.Plugins.monsoon.script.power_device import power_meter

class Monsoon(Profiler):
    def __init__(self, config, paths):
        super(Monsoon, self).__init__(config, paths)
        self.output_dir = ''
        self.paths = paths
        self.profile = False
        self.data_points = ["energy_joules", "duration_ms", "error_flag"]
        power_meter.monsoon_usb_enabled(True)


    def send_command(self, id, cmd):
        proc = subprocess.Popen(["adb", "-s", "01ca4c64db5d1014", "shell",  cmd],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate() 
        print("Jaaa returned")
        out = out.decode('ascii')
        print(out)
        if err:
            err = err.decode("ascii")
            print(err)
        time.sleep(5)

    def dependencies(self):
        return []

    def load(self, device):
        return

    def set_file(self, value):
        profiling_file = "/home/omar/profiling.txt"
        with open(profiling_file, 'w') as filetowrite:
            filetowrite.write(value)

    def start_profiling(self, device, **kwargs):
        """Start the profiling process"""

        # Quickly let the mobile device sleep and wake up so a run can take up to 30 minutes.
        # print("Sleep before profiling")
        # # device.shell("input keyevent KEYCODE_SLEEP")
        # self.send_command("01ca4c64db5d1014", "input keyevent KEYCODE_SLEEP")
        # print("Wake up before profiling")
        # self.send_command("01ca4c64db5d1014", "input keyevent KEYCODE_WAKEUP")
        # self.send_command("01ca4c64db5d1014", "input touchscreen swipe 530 1420 530 1120")
        # self.send_command("01ca4c64db5d1014", "input text 0000")
        # self.send_command("01ca4c64db5d1014", "input keyevent 66")
        # print("Wait for 5 seconds to be sure")
        # print("Wait for 5 secs after stopping profiling")
        # print("disbale USB Monsoon")

        self.set_file("1")


        power_meter.monsoon_usb_enabled(False)
        time.sleep(5)
        print("Really Start Profiling Now")
        self.start = datetime.datetime.now()
        self.profile = True
        power_meter.start()

    def stop_profiling(self, device, **kwargs):
        """Stop the profiling process"""
        self.results = power_meter.stop()
        self.end = datetime.datetime.now()
        delta = self.end - self.start 
        final = delta.total_seconds() * 1000
        print("Tijd ertussen", final)
        self.profile = False
        print("Wait for 5 secs after stopping profiling")
        # print("enable USB Monsoon")
        power_meter.monsoon_usb_enabled(True)
        self.set_file("0")
        time.sleep(5)
        # Quickly let the mobile device sleep and wake up so the device is awake for 30 minutes.
        # This solves the issue of certain commands sent to the device blocking the execution of the program.
        # print("Sleep after profiling")
        # device.shell("input keyevent KEYCODE_SLEEP")
        # device.shell("input keyevent KEYCODE_WAKEUP")
        # device.shell("input touchscreen swipe 530 1420 530 1120")
        # device.shell("input text 0000")
        # device.shell("input keyevent 66")
        # time.sleep(5)
        # print("Woken up")


    def collect_results(self, device):
        """Collect the data and clean up extra files on the device, save data in location set by 'set_output' """
        filename = 'monsoon_{}.csv'.format(time.strftime('%Y.%m.%d_%H%M%S'))
        with open(op.join(self.output_dir, filename), 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(self.data_points)
            #Seconds to milliseconds
            writer.writerow([self.results[0], round(self.results[1]*1000), self.results[2]])

    def unload(self, device):
        return

    def set_output(self, output_dir):
        """Set the output directory before the start_profiling is called"""
        self.output_dir = output_dir

    def aggregate_subject(self):
        """Aggregate the data at the end of a subject, collect data and save data to location set by 'set output' """
        with open(op.join(self.output_dir, 'aggregated.csv'), 'w+') as output:
            writer = csv.writer(output)
            writer.writerow(self.data_points)

            # Write data for each run to file in ascending order (oldest run first, newest run last).
            for output_file in sorted(os.listdir(self.output_dir), reverse=False):
                if output_file.startswith("monsoon_"):
                    res = open(op.join(self.output_dir, output_file)).readlines()[1]
                    res = res.rstrip()
                    res = res.split(",")
                    writer.writerow([res[0],res[1],res[2]])

    def aggregate_end(self, data_dir, output_file):
        """Aggregate the data at the end of the experiment.
         Data located in file structure inside data_dir. Save aggregated data to output_file
        """
        rows = self.aggregate_final(data_dir)
        util.write_to_file(output_file, rows)

    def aggregate_final(self, data_dir):
        """Compiles subject aggregation files"""
        rows = []
        for device in util.list_subdir(data_dir):
            row = OrderedDict({'device': device})
            device_dir = os.path.join(data_dir, device)
            for subject in util.list_subdir(device_dir):
                row.update({'subject': subject})
                subject_dir = os.path.join(device_dir, subject)
                if os.path.isdir(os.path.join(subject_dir, 'monsoon')):
                    temp_row = row.copy()
                    row.update(self.get_aggregated_runs_subject(
                        os.path.join(subject_dir, 'monsoon')))
                    self.add_rows(row, temp_row, rows, subject_dir)

                else:
                    for browser in util.list_subdir(subject_dir):
                        row.update({'browser': browser})
                        browser_dir = os.path.join(subject_dir, browser)
                        if os.path.isdir(os.path.join(browser_dir, 'monsoon')):
                            temp_row = row.copy()
                            row.update(self.get_aggregated_runs_subject(
                                os.path.join(browser_dir, 'monsoon')))
                            self.add_rows(row, temp_row, rows, browser_dir)
            return rows

    @staticmethod
    def get_aggregated_runs_subject(logs_dir):
        """Finds the aggregated file for a subject and returns the rows of that file.  The data returned is a key-value pair where the value is a list"""
        for aggregated_file in [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f))]:
            if aggregated_file == "aggregated.csv":
                with open(os.path.join(logs_dir, aggregated_file), 'r') as aggregated:
                    reader = csv.DictReader(aggregated)
                    row_dict = OrderedDict()
                    for row in reader:
                        for f in reader.fieldnames:
                            if f in row_dict.keys():
                                temp = row_dict[f]
                                temp.append(row[f])
                                row_dict.update({f: temp})
                            else:
                                row_dict.update({f: [row[f]]})
                    return OrderedDict(row_dict)

    def add_rows(self, row, temp_row, rows, dir):
        """Retrieves the list values in the key-value pairs from get_aggregated_runs_subject and creates n rows for list of size n"""
        repetition_count = len(os.listdir(os.path.join(dir, 'monsoon'))) - 1
        for i in range(repetition_count):
            temp_row.update({self.data_points[0]: row[self.data_points[0]][i], self.data_points[1]: row[self.data_points[1]][i], self.data_points[2]: row[self.data_points[2]][i]})
            rows.append(temp_row.copy())
        return rows
