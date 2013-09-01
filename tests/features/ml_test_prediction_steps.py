import os
import time
import csv
import json
from lettuce import step, world
from subprocess import check_call, CalledProcessError

@step(r'I create BigML multi-label resources with "(.*)" label separator and (\d*) labels uploading train "(.*)" file with "(.*)" field separator to test "(.*)" and log predictions in "(.*)"')
def i_create_all_ml_resources(step, label_separator=None, number_of_labels=None, data=None, training_separator=None, test=None, output=None):
    if label_separator is None or training_separator is None or number_of_labels is None or data is None or test is None or output is None:
        assert False
    world.directory = os.path.dirname(output)
    world.folders.append(world.directory)
    world.number_of_models = int(number_of_labels)
    try:
        command = "bigmler --multi-label --train " + data + " --label-separator \"" + label_separator + "\" --training-separator \"" + training_separator + "\" --test " + test + " --store --output " + output + " --max-batch-models 1"
        retcode = check_call(command, shell=True)
        if retcode < 0:
            assert False
        else:
            world.test_lines = 0
            for line in open(test, "r"):
                world.test_lines += 1
            world.output = output
            assert True
    except (OSError, CalledProcessError, IOError) as exc:
        assert False, str(exc)
