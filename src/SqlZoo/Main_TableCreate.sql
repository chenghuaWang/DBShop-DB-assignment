USE Shop;
CREATE TABLE C(
    CNo     CHAR(10)    CHECK(CNo LIKE 'C[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    CName   VARCHAR(10) NOT NULL,
    CPhone  CHAR(12)    CHECK(CPhone LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    CAddr   VARCHAR(100)NOT NULL,
    PRIMARY KEY (CNo),
);

CREATE TABLE S(
    SNo     CHAR(10)    CHECK(SNo LIKE 'S[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    SName   VARCHAR(50) NOT NULL,
    SKind   VARCHAR(30) NOT NULL,
    SPrice  FLOAT       CHECK(SPrice >= 0),
    SInventory  INT     CHECK(SInventory >= 0),
    PRIMARY KEY (SNo),
);

CREATE TABLE G(
    GNo     CHAR(10)    CHECK(GNo LIKE 'G[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    CNo     CHAR(10)    CHECK(CNo LIKE 'S[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    PRIMARY KEY (GNo),
);

CREATE TABLE D(
    DNo     CHAR(10)    CHECK(DNo LIKE 'G[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    CNo     CHAR(10)    CHECK(CNo LIKE 'S[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    DPay    FLOAT,
    DPay_yn BIT         NOT NULL,
    DS_yn   BIT         NOT NULL,
    DM_yn   FLOAT,
    PRIMARY KEY (DNo),
)

CREATE TABLE GS(
    SNo     CHAR(10)    CHECK(SNo LIKE 'S[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    GNo     CHAR(10)    CHECK(GNo LIKE 'G[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    GSNum   INT,
    PRIMARY KEY (SNo),
)

CREATE TABLE DS(
    SNo     CHAR(10)    CHECK(SNo LIKE 'S[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    DNo     CHAR(10)    CHECK(DNo LIKE 'G[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    DSNum   INT         CHECK(DSNum >= 0),
    PRIMARY KEY (SNo),
)

CREATE TABLE GG(
    GGNo    CHAR(10)    CHECK(GGNo LIKE 'P[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    SNo     CHAR(10)    CHECK(SNo LIKE 'G[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    GGName  VARCHAR(50) NOT NULL,
    GGAddr  VARCHAR(100)NOT NULL, 
    PRIMARY KEY (GGNo),
);

ALTER TABLE G ADD CONSTRAINT fk_G_CNo FOREIGN KEY (CNo) REFERENCES C(CNo);
ALTER TABLE D ADD CONSTRAINT fk_D_CNo FOREIGN KEY (CNo) REFERENCES C(CNo);
ALTER TABLE GS ADD CONSTRAINT fk_GS_GNo FOREIGN KEY (GNo) REFERENCES G(GNo);
ALTER TABLE DS ADD CONSTRAINT fk_DS_DNo FOREIGN KEY (DNo) REFERENCES D(DNo);
ALTER TABLE GG ADD CONSTRAINT fk_GG_SNo FOREIGN KEY (SNo) REFERENCES S(SNo);