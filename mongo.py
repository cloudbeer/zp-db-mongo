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


"""
    This package is base data access for mongodb.
    这个包是访问 mongodb 的基础包

    Depends on pymongo
    依赖 pymongo
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from fields import zpstr

def zpid(val = None, create_new = False):
    """
    Transfer value to bson objectid
    将值转化成为 bson 的 objectid

    return objectid if right value else create new one or return None
    返回一个 objectid 对象，或者创建一个新的，或者返回 None
    """
    try:
        if (isinstance(val, ObjectId)):
            return val
        if (isinstance(val, str)):
            return ObjectId(val)

    except:
        if (create_new): return ObjectId()
        else: return None




class field:
    '''
    This is field/col
    '''
    def __init__(self, init_type = zpstr, init_value = None,):
        self.ztype = init_type
        self.zval = init_value

    def val(self, new_val = None):
        '''
        just like jQuery, getter or setter.
        '''
        if(new_val != None):
            if (self is not None): self.zval = new_val
        else:
            if (self is None): return None
            return self.zval

class entity(dict):
    '''
    这个是实体的基类
    '''
    __table__ = None

    def __getattr__(self, name):
        if (self.has_key(name)):
            return self[name]
        else:
            return field(init_value=None)
    def __setattr__(self, name, value):
        self[name] = value

    def dump(self):
        '''
        Have a look
        将实例中的属性和值输出出来

        '''
        if (self is None):
            return None
        xdict = dict()
        print(self.keys())
        for k in self:
            print (0)
            xdict[k] = self[k].val()
        return (xdict)

    def bind(self, xdict):
        '''
        将字典数据绑定到实体，在web.py中可以直接将web.input 绑定进来

        '''
        if (xdict is None): return None

        for k in self:
            xvalue = xdict[k] if xdict.has_key(k) else None
            self[k].val(xvalue)

    def id(self):
        return self._id.val()



class entities:
    def __init__(self):
        self.list = []

        self.count = 0
        self.size = 10
        self.page = 1
        self.pagecount = 1


    #TODO: 这个需要改造成多组分页显示
    def pager(self):
        if (self.pagecount == 1):
            return ""
        prev_page = self.page - 1 if self.page - 1 > 0 else 1
        next_page = self.page + 1 if self.page + 1 <= self.pagecount else self.pagecount
        html = '\
    <div class="pagination">\
        <ul>\
        '
        if (self.page > 1):
            html += '<li><a href="#" data-page="' + str(prev_page) + '">前页</a></li>'
        else:
            html += '<li class="disabled"><a href="#" data-page="' + str(prev_page) + '">前页</a></li>'
        for i in range(1, self.pagecount+1):
            if (i == self.page):
                html += '<li class="disabled"><a href="#" data-page="' + str(i) + '">' + str(i) + '</a></li>'
            else:
                html += '<li><a href="#" data-page="' + str(i) + '">' + str(i) + '</a></li>'
        if self.page < self.pagecount:
            html += '<li><a href="#" data-page="' + str(next_page) + '">后页</a></li>'
        else:
            html += '<li class="disabled"><a href="#" data-page="' + str(next_page) + '">后页</a></li>'
        html += '\
        </ul>\
    </div>'
        return html


#TODO: 此处需要写入配置文件, 目前在测试
#def db():
#    connection = MongoClient('localhost') 
#    return connection.mongo_store
# 目前我还不知道如何把这个配置挪出去啊，救命啊
connection = MongoClient('localhost')
db = connection.mongo_store


def insert(instance):
    '''
    Save an entity to db collection
    将实体插入数据库中

    '''
    x_dict = dict()
    for k in instance:
        ori_val = instance[k].val()
        lst_val = instance[k].ztype(ori_val)
        x_dict[k] = lst_val
    try:
        del x_dict['_id']
    except:
        pass

    db[instance.__table__].insert(x_dict)

#TODO: UPDATE有bug，这个bug需要处理  
def update(instance, where = None):
    '''
    Update an entity to db collection.
    更新实体。

    if where is None, where's key is _id.
    如果未指定 where 字段，则使用 _id 作为更新条件。
    '''

    x_dict = dict()
    for k in instance:
        ori_val = instance[k].val()
        lst_val = instance[k].ztype(ori_val)
        if (lst_val is not None and k != '_id'):
            x_dict[k] = lst_val
        if (k == '_id'):
            pk_val = lst_val

        x_dict[k] = lst_val
    if (where == None and pk_val is not None):
        where = {'_id': pk_val}


    if (where == None):
        raise ValueError()

    db[instance.__table__].update(where, {"$set": x_dict})


def find_one(entity_type, where = None, _id = None):
    '''
    查询出满足条件的一个记录，并把它放入实体
    '''
    if (where == None):
        where = dict()
    if (_id != None):
        where["_id"] = zpid(str(_id))
    x_dict = db[entity_type.__table__].find_one(where)
    if (x_dict is None): return None
    instance = entity_type()
    instance.bind(x_dict)
    return instance



def find(entity_type, where = None, orderby = None, size = 20, page = 1):
    '''
    查询出满足条件的一个记录，并把它放入实体
    '''
    list_all = db[entity_type.__table__].find(where)
    if (list_all is None): return None
    count = list_all.count()
    if (orderby is not None):
        list_all.sort(orderby[0], orderby[1])

    page_count = count / size if count % size == 0 else count / size + 1
    page = page if page <= page_count else page_count
    page = page if page>0 else 1
    offset = size * (page - 1)

    bindsList = entities()
    bindsList.count = count
    bindsList.page = page
    bindsList.pagecount = page_count
    bindsList.size = size

    x_dict_list = list_all.skip(offset).limit(size)
    for x_dict in x_dict_list:
        instance = entity_type()
        instance.bind(x_dict)
        bindsList.list.append(instance)
    return bindsList








