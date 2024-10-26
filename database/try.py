import sql

test1={"id": "1",
      "type": "City",
      "name": "北京",
      "coordinates": {
        "latitude": 12.2332,
        "longitude": 123.3232
      }
    }
test2={
      "id": "11",
      "type": "Region",
      "name": "北京市海淀区",
      "coordinates": {
        "latitude": 13.1313,
        "longitude": 134.2323
      }
    }
test3={
      "id": "111",
      "type": "AOI",
      "name": "北京理工大学",
      "coordinates": {
        "latitude": 14.1414,
        "longitude": 145.6767
      }
    }
test4={
      "id": "1111",
      "type": "POI",
      "name": "北京理工大学中心教学楼",
      "coordinates": {
        "latitude": 15.1212,
        "longitude": 156.7878
      }
    }
test5={
      "id": "1112",
      "type": "POI",
      "name": "北京理工大学计算机学院",
      "coordinates": {
        "latitude": 15.1212,
        "longitude": 156.7878
      }
    }
test6={
      "id": "112",
      "type": "AOI",
      "name": "中国人民大学",
      "coordinates": {
        "latitude": 14.1414,
        "longitude": 145.6767
      }
    }

test7={"id": "2",
      "type": "City",
      "name": "天津",
      "coordinates": {
        "latitude": 13.2332,
        "longitude": 133.3232
      }
    }

relation1={
      "id": "1",
      "type": "LocatedIn",
      "from": "1",
      "to": "11"
    }
relation2={
      "id": "11",
      "type": "LocatedIn",
      "from": "11",
      "to": "111"
    }
relation3={
      "id": "1111",
      "type": "SameAs",
      "from": "1111",
      "to": "1112"
    }
relation4={
      "id": "111",
      "type": "CloseTo",
      "from": "111",
      "to": "112"
    }
# sql.sqlAdd(test1)
# sql.sqlAdd(test2)
# sql.sqlAdd(test3)
# sql.sqlAdd(test4)
# sql.sqlAdd(test5)
# sql.sqlAdd(test6)
sql.sqlAdd(test7)
# sql.sqlAdd(relation1)
# sql.sqlAdd(relation2)
# sql.sqlAdd(relation3)
# sql.sqlAdd(relation4)
# sql.sqlDelete(111,regionalism="AOI",relation="CloseTo")
# sql.sqlDelete(1,relation="LocatedIn")
# sql.sqlDelete(1)
res = sql.sqlSelect("City")
print(res)
# res = sql.sqlSelect(relation="locatedin")
# print(res)
# print(sql.sqlTables())