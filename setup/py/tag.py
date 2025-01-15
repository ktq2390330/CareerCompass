import os
import logging
import datetime
from django_setup_def import djangoImportSetup
djangoImportSetup()
from CCapp.models import *
from CCapp.defs import makeDirFile,makeImportPath,logconfig,logException,logsOutput,readFile,executeFunction
from django.db import transaction
import csv
import random
from itertools import cycle

