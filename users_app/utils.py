from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth import login, authenticate, logout
import sys
