-- CREATE TABLE S(
--     SNo     CHAR(10)    CHECK(SNo LIKE 'S[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
--     SName   VARCHAR(50) NOT NULL,
--     SKind   VARCHAR(30) NOT NULL,
--     SPrice  FLOAT       CHECK(SPrice >= 0),
--     SInventory  INT     CHECK(SInventory >= 0),
--     PRIMARY KEY (SNo),
-- );
USE Shop;
INSERT Into S VALUES ('S00000100','雪碧','饮品','3 ','5000');
INSERT Into S VALUES ('S00000101','可乐','饮品','3 ','4500');
INSERT Into S VALUES ('S00000102','矿泉水','饮品','2 ','6000');
INSERT Into S VALUES ('S00000103','球鞋','衣着','1500 ','200');
INSERT Into S VALUES ('S00000104','衬衫','衣着','50 ','500');
INSERT Into S VALUES ('S00000105','电脑','电器','5450 ','100');
INSERT Into S VALUES ('S00000106','冰箱','电器','1500 ','200');
INSERT Into S VALUES ('S00000107','洗衣机','电器','700 ','300');
INSERT Into S VALUES ('S00000108','手表','生活用品','340 ','200');
INSERT Into S VALUES ('S00000109','纸巾','生活用品','4 ','2000');