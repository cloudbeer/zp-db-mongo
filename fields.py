# coding: utf-8

# Copyright 2012-2013 zippy project.
# author: cloudbeer (cloudbeer@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You
# may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.

from datetime import datetime

def zpint(val):
    """
    Transfer value to integer

    return integer if right value else None
    """
    try:
        return int(val)
    except:
        return None

def zpstr(val):
    """
    Transfer value to string

    return string if right value
    """
    return unicode(val) if val is not None else None

def zpdatetime(val):
    """
    Transfer value (must be as '2012-11-12') to date

    return datetime if right value else None
    """
    try:
        return val if isinstance(val, datetime) else datetime.strptime(val,'%Y-%m-%d')
    except:
        return None

def zpfloat(val):
    """
    Transfer value to float

    return float if right value else None
    """
    try:
        return float(val)
    except:
        return None

def zpnone(val):
    return None


