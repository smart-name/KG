import pymysql
import threading


class SqlConnect(object):
    _instance_lock = threading.Lock()
    _password = '1234567890'

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SqlConnect, "_conn"):
            with SqlConnect._instance_lock:
                if not hasattr(SqlConnect, "_conn"):
                    # SqlConnect._conn = pymysql.connect(host='localhost', user='root', password=SqlConnect._password,
                    #                                    database='city_knowledge_graph')
                    SqlConnect._conn = pymysql.connect(host='localhost', user='root', password=SqlConnect._password,
                                                       database='city_knowledge_graph_test')
        return SqlConnect._conn

def sqlTables():
    conn = SqlConnect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    commamd = "show tables"
    cursor.execute(commamd)
    result = cursor.fetchall()
    conn.commit()
    return result

def sqlSelect(table, condition, showcoordinates, column):
    conn = SqlConnect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # 如果column为空输入则查询全部
    if not column:
        column = "*"

    if showcoordinates and "_" in table:
        locatedin = {"city":"region", "region":"aoi", "aoi":"poi"}
        entity_relation = table.split("_")
        entity = entity_relation[0]
        relation = entity_relation[1]
        #获取当前表的列名
        if column == "*":
            command = "select * from " + table
            cursor.execute(command)
            attrs = list(cursor.fetchone().keys())
        else:
            attrs = column.split(",")
        #进行重新拼接
        need_split = False
        column_origin = ""
        column_as = ""

        for attr in attrs:
            if need_split:
                column_origin += ","
                column_as += ","
            else:
                need_split =True

            if attr == "id":
                column_origin += table + ".id" + " as id"
                column_as += "id"
            elif attr == "idFrom":
                column_origin += "idFrom,temp_table1.name as idFrom_name"
                column_as += "idFrom,idFrom_name"
            elif attr == "idTo":
                column_origin += "idTo,temp_table2.name as idTo_name"
                column_as += "idTo,idTo_name"
            else:
                column_origin += attr
                column_as += attr

        command = "select " + column_origin + " from " + table + " left join " + entity + " as temp_table1 on temp_table1.id=" + table + ".idFrom"

        if relation == "closeto" or relation == "sameas":
            command += " left join " + entity + " as temp_table2 on temp_table2.id=" + table + ".idTo"
        elif relation == "locatedin":
            command += " left join " + locatedin[entity] + " as temp_table2 on temp_table2.id=" + table + ".idTo"

    else:
        command = "select "+ column + " from " + table

    if condition:
        command += " where "+ condition
    # print(command)
    cursor.execute(command)
    results = cursor.fetchall()

    conn.commit()
    return results

def sqlAdd(data, type):
    """data需为某一实体/关系的字典形式"""
    # 重写下regionalismlist
    conn = SqlConnect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    regionalismlist = {"City", "Region", "AOI", "POI"}

    # if "coordinates" in data.keys():
    if type == "entities":
        command = "insert into " + data["type"] + " values (" + data["id"] + ",\"" + data["name"] + "\")"
        # print(command)
        cursor.execute(command)
        #先按只有1对经纬度写
        command = "insert into "+data["type"]+"_Coordinates(idFrom,latitude,longitude) values ("+data["id"]+","+str(data["coordinates"]["latitude"])+","+str(data["coordinates"]["latitude"])+")"
        # print(command)
        cursor.execute(command)
    # elif "from" and "to" in data.keys():
    elif type == "relations":
        for entity in regionalismlist:
            command = "select * from " + entity + " where id=" + data["from"]
            effect_row = cursor.execute(command)
            if effect_row > 0:
                command = "insert into " + entity + '_' + data["type"] + " values (" + data["id"] + "," + data["from"] + "," + data["to"] + ")"
                cursor.execute(command)
                break
    else:
        print("非法输入")
    conn.commit()

def sqlDelete(table, condition):
    conn = SqlConnect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    regionalismlist = {"city", "region", "aoi", "poi"}

    if table in regionalismlist:
        # 如果是实体先删除coordinates里的
        results = sqlSelect(table, condition=condition, showcoordinates=None, column="id")
        for result in results:
            command = "delete from " + table + "_Coordinates where idFrom=" + str(result["id"])
            cursor.execute(command)

    #再删除其他的
    command = "delete from " + table + " where " + condition
    cursor.execute(command)
    conn.commit()

def sqlUpdate(table, column, condition):
    conn = SqlConnect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    command = "update " + table + " set " + column
    if condition:
        command += " where " + condition
    cursor.execute(command)
    conn.commit()




# cursor.close()
# conn.close()
# conn = SqlConnect()
# cursor = conn.cursor(pymysql.cursors.DictCursor)
# command = "select id from city_locatedin left join city on city_locatedin.idfrom=city.id left join city as city1 on city_locatedin.idto=region.id "
# command = "select * from city_locatedin left join city on city_locatedin.idfrom=city.id left join region on city_locatedin.idto=region.id "
# cursor.execute(command)
# results = cursor.fetchall()
# results = cursor.fetchone().keys()
# results = sqlSelect("city_coordinates","","on")
# print(results)
# print(list(results))
# print(type(results))
