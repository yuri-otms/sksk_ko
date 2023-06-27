-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: sksk_ko
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `e_group`
--

DROP TABLE IF EXISTS `e_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `e_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `grade` int DEFAULT NULL,
  `e_group` varchar(100) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `position` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `grade` (`grade`),
  CONSTRAINT `e_group_ibfk_1` FOREIGN KEY (`grade`) REFERENCES `grade` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `e_group`
--

LOCK TABLES `e_group` WRITE;
/*!40000 ALTER TABLE `e_group` DISABLE KEYS */;
INSERT INTO `e_group` VALUES (1,1,'1. 指示詞、存在詞、数詞','입니다, 있다, 하나',1),(2,1,'2. 用言・ㄹ語幹・否定','갑니다, 알다, 지 않다',2),(3,1,'3.','',3),(5,NULL,'新規グループ','新規グループ',1),(6,NULL,'新規グループ','新規グループ',1),(7,NULL,'新規グループ','新規グループ',1),(8,6,'新規グループ','新規グループ',1),(10,1,'4.','',4),(11,NULL,'新規グループ','新規グループ',1),(12,NULL,'新規グループ','新規グループ',1);
/*!40000 ALTER TABLE `e_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `element`
--

DROP TABLE IF EXISTS `element`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `element` (
  `id` int NOT NULL AUTO_INCREMENT,
  `e_group` int DEFAULT NULL,
  `element` varchar(40) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `position` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `e_group` (`e_group`),
  CONSTRAINT `element_ibfk_1` FOREIGN KEY (`e_group`) REFERENCES `e_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `element`
--

LOCK TABLES `element` WRITE;
/*!40000 ALTER TABLE `element` DISABLE KEYS */;
INSERT INTO `element` VALUES (1,1,'指示詞','입니다',1),(2,1,'指示詞の否定','아닙니다',2),(3,1,'存在詞','았다, 없다',3),(4,1,'固有数詞','하나, 둘, 셋',4),(5,1,'漢数詞','일, 이, 삼',5),(6,1,'疑問詞(いつ、どこ、いくら)','언제, 어디, 얼마',6),(7,2,'ハムニダ体用言','갑니다, 읽습니다',1),(8,3,'項目1','一つ目の項目',1),(9,NULL,'項目1','一つ目の項目',1),(10,5,'新規項目','新規項目',1),(11,2,'ㄹ語幹用言','알다, 멀다',2),(12,2,'를/을 をとる動詞','좋아하다, 만나다',3),(13,5,'新規項目','新規項目',2),(14,5,'新規項目','新規項目',3),(15,NULL,'項目1','一つ目の項目',1),(16,10,'項目1','一つ目の項目',1),(18,5,'新規項目','新規項目',4),(19,5,'新規項目','新規項目',5),(20,2,'助詞(1)','에서, 로, 에게',4),(21,2,'否定(1)','안',5);
/*!40000 ALTER TABLE `element` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grade`
--

DROP TABLE IF EXISTS `grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grade` (
  `id` int NOT NULL AUTO_INCREMENT,
  `grade` varchar(30) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `position` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `grade` (`grade`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grade`
--

LOCK TABLES `grade` WRITE;
/*!40000 ALTER TABLE `grade` DISABLE KEYS */;
INSERT INTO `grade` VALUES (1,'ハン検5級','입니다, 고 싶다, ㄹ까요',1),(6,'ハン検4級','',2);
/*!40000 ALTER TABLE `grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hint`
--

DROP TABLE IF EXISTS `hint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hint` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` int DEFAULT NULL,
  `word` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question` (`question`),
  KEY `word` (`word`),
  CONSTRAINT `hint_ibfk_1` FOREIGN KEY (`question`) REFERENCES `question` (`id`) ON DELETE CASCADE,
  CONSTRAINT `hint_ibfk_2` FOREIGN KEY (`word`) REFERENCES `word` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hint`
--

LOCK TABLES `hint` WRITE;
/*!40000 ALTER TABLE `hint` DISABLE KEYS */;
INSERT INTO `hint` VALUES (3,2,3),(4,3,4),(5,3,5),(6,4,6),(7,5,7),(8,5,8),(9,6,9),(10,6,10),(11,7,11),(12,7,12),(13,8,13),(14,9,14),(15,10,15),(16,11,16),(17,12,17),(18,1,18),(19,1,2),(20,12,19),(21,13,20),(22,13,21),(23,14,22),(24,14,23),(25,15,4),(26,15,24),(27,21,9),(28,21,25),(29,21,26),(31,22,18),(32,22,27),(33,23,28);
/*!40000 ALTER TABLE `hint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `level`
--

DROP TABLE IF EXISTS `level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `level` (
  `id` int NOT NULL AUTO_INCREMENT,
  `level` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `level`
--

LOCK TABLES `level` WRITE;
/*!40000 ALTER TABLE `level` DISABLE KEYS */;
INSERT INTO `level` VALUES (1,1);
/*!40000 ALTER TABLE `level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `privilege`
--

DROP TABLE IF EXISTS `privilege`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `privilege` (
  `id` int NOT NULL AUTO_INCREMENT,
  `privilege` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `privilege`
--

LOCK TABLES `privilege` WRITE;
/*!40000 ALTER TABLE `privilege` DISABLE KEYS */;
INSERT INTO `privilege` VALUES (1,'編集'),(2,'確認'),(3,'承認'),(4,'管理');
/*!40000 ALTER TABLE `privilege` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `process`
--

DROP TABLE IF EXISTS `process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `process` (
  `id` int NOT NULL AUTO_INCREMENT,
  `process` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `process`
--

LOCK TABLES `process` WRITE;
/*!40000 ALTER TABLE `process` DISABLE KEYS */;
INSERT INTO `process` VALUES (1,'作成'),(2,'編集'),(3,'削除'),(4,'確認依頼'),(5,'確認済み'),(6,'確認却下'),(7,'再提出'),(8,'公開'),(9,'非公開');
/*!40000 ALTER TABLE `process` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `id` int NOT NULL AUTO_INCREMENT,
  `element` int DEFAULT NULL,
  `level` int DEFAULT NULL,
  `japanese` varchar(100) DEFAULT NULL,
  `foreign_l` varchar(100) DEFAULT NULL,
  `style` int DEFAULT NULL,
  `spoken` tinyint(1) NOT NULL,
  `sida` tinyint(1) NOT NULL,
  `will` tinyint(1) NOT NULL,
  `position` int DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `created_by` int DEFAULT NULL,
  `process` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `element` (`element`),
  KEY `level` (`level`),
  KEY `style` (`style`),
  KEY `created_by` (`created_by`),
  KEY `process` (`process`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`element`) REFERENCES `element` (`id`) ON DELETE CASCADE,
  CONSTRAINT `question_ibfk_2` FOREIGN KEY (`level`) REFERENCES `level` (`id`) ON DELETE CASCADE,
  CONSTRAINT `question_ibfk_3` FOREIGN KEY (`style`) REFERENCES `style` (`id`) ON DELETE CASCADE,
  CONSTRAINT `question_ibfk_4` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `question_ibfk_5` FOREIGN KEY (`process`) REFERENCES `process` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,1,1,'父は医者です。','아버지는 의사입니다.',1,0,0,0,1,'2023-03-10 09:50:35',2,8),(2,1,1,'私は学生です。','저는 학생입니다.',1,0,0,0,2,'2023-03-10 09:50:35',2,8),(3,1,1,'母は公務員です。','어머니는 공무원입니다.',1,0,0,0,3,'2023-03-10 09:50:35',2,8),(4,1,1,'私のカバンですか？','제 가방입니까?',1,0,0,0,4,'2023-03-10 09:50:35',2,8),(5,1,1,'これはキムチですか？','이것은 김치입니까?',1,0,0,0,5,'2023-03-10 09:50:35',2,8),(6,2,1,'今日は休日ではありません。','오늘은 휴일이 아닙니다.',1,0,0,0,1,'2023-03-10 09:51:37',2,8),(7,2,1,'ここは銀行ではありません。','여기는 은행이 아닙니다.',1,0,0,0,2,'2023-03-10 09:51:37',2,8),(8,2,1,'風邪ではありませんか？','감기가 아닙니까?',1,0,0,0,3,'2023-03-10 09:51:37',2,8),(9,2,1,'私のノートではありません。','제 노트가 아닙니다.',1,0,0,0,4,'2023-03-10 09:51:37',2,8),(10,2,1,'弟ではありません。','남동생이 아닙니다.',1,0,0,0,5,'2023-03-10 09:51:37',2,8),(11,3,1,'宿題があります。','숙제가 있습니다.',1,0,0,0,1,'2023-03-10 09:51:37',2,8),(12,3,1,'火曜日に試験があります。','화요일에 시험이 있습니다.',1,0,0,0,2,'2023-03-10 09:51:37',2,8),(13,3,1,'姉と妹がいます。','언니하고 여동생이 있습니다.',1,1,0,0,3,'2023-03-10 09:51:37',2,8),(14,3,1,'日曜日は授業がありませんか？','일요일은 수업이 없습니까?',1,0,0,0,4,'2023-03-10 09:51:37',2,8),(15,3,1,'母は家にいません。','어머니는 집에 없습니다.',1,0,0,0,5,'2023-03-10 09:51:37',2,8),(16,4,1,'私は26歳です。','저는 스물여섯 살입니다.',1,0,0,0,1,'2023-03-10 09:51:37',2,8),(17,4,1,'猫が2匹います。','고양이가 두 마리 있습니다.',1,0,0,0,2,'2023-03-10 09:51:37',2,8),(18,4,1,'りんごが3個あります。','사과가 세 개 있습니다.',1,0,0,0,3,'2023-03-10 09:51:38',2,8),(19,4,1,'部屋に本が9冊あります。','방에 책이 아홉 권 있습니다.',1,0,0,0,4,'2023-03-10 09:51:38',2,8),(20,4,1,'教室に学生が8人います。','교실에 학생이 여덟 명 있습니다.',1,0,0,0,5,'2023-03-10 09:51:38',2,8),(21,5,1,'今日は12月26日です。','오늘은 십이월 이십육 일입니다.',1,0,0,0,1,'2023-03-10 09:51:38',2,8),(22,5,1,'父の誕生日は6月3日です。','아버지 생일은 유월 삼일입니다.',1,0,0,0,2,'2023-03-10 09:51:38',2,8),(23,5,1,'このコンピューターは120万ウォンです。','이 컴퓨터는 백이십만원입니다.',1,0,0,0,3,'2023-03-10 09:51:38',2,8),(24,5,1,'姉の部屋は738号室です。','누나 방은 칠백삼십팔 호실입니다.',1,0,0,0,4,'2023-03-10 09:51:38',2,8),(25,5,1,'弟は5年生です。','남동생은 오학년입니다.',1,0,0,0,5,'2023-03-10 09:51:38',2,8),(26,6,1,'誕生日はいつですか？','생일은 언제입니까?',1,0,0,0,1,'2023-03-10 09:51:38',2,8),(27,6,1,'試験はいつありますか？','시험은 언제 있습니까?',1,0,0,0,2,'2023-03-10 09:51:38',2,8),(28,6,1,'銀行はどこですか？','은행은 어디입니까?',1,0,0,0,3,'2023-03-10 09:51:38',2,8),(29,6,1,'病院はどこにありますか？','병원은 어디에 있습니까?',1,0,0,0,4,'2023-03-10 09:51:38',2,8),(30,6,1,'このカバンはいくらですか？','이 가방은 얼마입니까?',1,0,0,0,5,'2023-03-10 09:51:38',2,8),(31,1,1,'あ','아',1,0,0,0,6,'2023-03-12 10:37:54',1,3),(32,7,1,'学校へ行きます。','학교에 갑니다.',1,0,0,0,1,'2023-03-12 14:58:16',1,8),(33,7,1,'ごはんを食べますか？','밥을 먹습니까?',1,0,0,0,2,'2023-03-12 14:58:16',1,8),(34,7,1,'手紙を読みます。','편지를 읽습니다.',1,0,0,0,3,'2023-03-12 14:58:16',1,8),(35,7,1,'忙しいですか？','바쁩니까?',1,0,0,0,4,'2023-03-12 14:58:16',1,8),(36,7,1,'このキムチはおいしいです。','이 김치는 맛있습니다.',1,0,0,0,5,'2023-03-12 14:58:16',1,8),(37,11,1,'兄を知っていますか？','오빠를 압니까?',1,0,0,0,1,'2023-03-12 18:33:41',2,8),(38,11,1,'母に電話をかけます。','어머니에게 전화를 겁니다.',1,0,0,0,2,'2023-03-12 18:33:41',2,8),(39,11,1,'駅は遠いですか？','역은 멉니까?',1,0,0,0,3,'2023-03-12 18:33:41',2,8),(40,11,1,'韓国料理を作ります。','한국 요리를 만듭니다.',1,0,0,0,4,'2023-03-12 18:33:41',2,8),(41,11,1,'ソウルに住んでいます。','서울에 삽니다.',1,0,0,0,5,'2023-03-12 18:33:41',2,8),(42,12,1,'私は中国料理が好きです。','저는 중국 요리를 좋아합니다.',1,0,0,0,1,'2023-03-13 12:26:58',1,8),(43,12,1,'空港で母に会います。','공항에서 어버니를 만납니다.',1,0,0,0,2,'2023-03-13 12:26:58',1,8),(44,12,1,'地下鉄に乗ります。','치하철을 탑니다.',1,0,0,0,3,'2023-03-13 12:26:58',1,8),(45,12,1,'旅行に行きます。','여행을 갑니다.',1,0,0,0,4,'2023-03-13 19:14:59',2,8),(46,12,1,'家で友達と遊びます。','집에서 친구와 놉니다.',1,0,0,0,5,'2023-03-13 19:14:59',2,8),(47,20,1,'バスで会社に行きます。','버스로 회사에 갑니다.',1,0,0,0,1,'2023-03-13 19:36:33',1,5),(48,20,1,'韓国語で本を読みます。','한국어로 책을 읽습니다.',1,0,0,0,2,'2023-03-13 19:36:33',1,5),(49,20,1,'家でビビンバを作ります。','집에서 비빔밥을 만듭니다.',1,0,0,0,3,'2023-03-13 19:36:33',1,1),(50,20,1,'公園で遊びます。','공원에서 놉니다.',1,0,0,0,4,'2023-03-13 19:36:33',1,1),(51,20,1,'犬に水をあげます。','개에게 물을 줍니다.',1,0,0,0,5,'2023-03-13 19:36:33',1,1);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_request`
--

DROP TABLE IF EXISTS `question_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_request` (
  `id` int NOT NULL AUTO_INCREMENT,
  `client` int DEFAULT NULL,
  `process` int DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `detail` text,
  `requested_at` datetime NOT NULL,
  `checked_by` int DEFAULT NULL,
  `finished_at` datetime DEFAULT NULL,
  `request_id` int DEFAULT NULL,
  `read` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client` (`client`),
  KEY `process` (`process`),
  KEY `checked_by` (`checked_by`),
  CONSTRAINT `question_request_ibfk_1` FOREIGN KEY (`client`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `question_request_ibfk_2` FOREIGN KEY (`process`) REFERENCES `process` (`id`) ON DELETE CASCADE,
  CONSTRAINT `question_request_ibfk_3` FOREIGN KEY (`checked_by`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_request`
--

LOCK TABLES `question_request` WRITE;
/*!40000 ALTER TABLE `question_request` DISABLE KEYS */;
INSERT INTO `question_request` VALUES (1,2,5,'問題文の確認依頼','','2023-03-10 09:51:50',1,'2023-03-10 09:52:45',0,0),(2,1,5,'問題文の確認依頼','','2023-03-12 17:56:10',1,'2023-03-12 17:56:23',0,0),(3,1,5,'問題文の確認依頼','','2023-03-12 17:56:38',3,'2023-03-12 18:49:50',0,0),(4,2,3,'問題文の確認依頼','','2023-03-12 18:38:29',NULL,NULL,0,0),(5,2,5,'問題文の確認依頼','','2023-03-12 18:40:03',3,'2023-03-12 18:41:57',0,0),(6,2,5,'問題文の確認依頼','','2023-03-12 18:49:33',3,'2023-03-12 18:50:55',0,0),(7,2,5,'問題文の確認依頼(再提出)','','2023-03-12 18:58:02',1,'2023-03-13 08:30:22',6,0),(8,1,5,'問題文の確認依頼','','2023-03-13 05:46:44',1,'2023-03-13 08:30:31',0,0),(9,1,5,'問題文の確認依頼','','2023-03-13 17:00:57',1,'2023-03-13 17:01:07',0,0),(10,1,5,'問題文の確認依頼(再提出)','','2023-03-13 19:25:05',1,'2023-03-13 19:27:16',3,0),(11,2,5,'問題文の確認依頼','','2023-03-13 19:28:15',1,'2023-03-13 19:28:43',0,0),(12,1,5,'問題文の確認依頼','','2023-03-13 19:36:45',1,'2023-03-13 19:36:52',0,0),(13,1,5,'問題文の確認依頼(再提出)','','2023-03-13 19:39:14',1,'2023-03-13 19:39:23',12,0),(14,1,5,'問題文の確認依頼','','2023-03-13 19:39:28',1,'2023-03-13 19:39:40',0,0),(15,1,5,'問題文の確認依頼(再提出)','','2023-03-13 19:39:48',1,'2023-03-13 19:40:23',14,0);
/*!40000 ALTER TABLE `question_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `record`
--

DROP TABLE IF EXISTS `record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` int DEFAULT NULL,
  `question` int DEFAULT NULL,
  `process` int DEFAULT NULL,
  `message` text,
  `executed_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user` (`user`),
  KEY `process` (`process`),
  CONSTRAINT `record_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `record_ibfk_2` FOREIGN KEY (`process`) REFERENCES `process` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
INSERT INTO `record` VALUES (1,2,1,1,'なし','2023-03-10 09:50:35'),(2,2,2,1,'なし','2023-03-10 09:50:35'),(3,2,3,1,'なし','2023-03-10 09:50:35'),(4,2,4,1,'なし','2023-03-10 09:50:35'),(5,2,5,1,'なし','2023-03-10 09:50:35'),(6,2,6,1,'なし','2023-03-10 09:51:37'),(7,2,7,1,'なし','2023-03-10 09:51:37'),(8,2,8,1,'なし','2023-03-10 09:51:37'),(9,2,9,1,'なし','2023-03-10 09:51:37'),(10,2,10,1,'なし','2023-03-10 09:51:37'),(11,2,11,1,'なし','2023-03-10 09:51:37'),(12,2,12,1,'なし','2023-03-10 09:51:37'),(13,2,13,1,'なし','2023-03-10 09:51:37'),(14,2,14,1,'なし','2023-03-10 09:51:37'),(15,2,15,1,'なし','2023-03-10 09:51:37'),(16,2,16,1,'なし','2023-03-10 09:51:37'),(17,2,17,1,'なし','2023-03-10 09:51:37'),(18,2,18,1,'なし','2023-03-10 09:51:38'),(19,2,19,1,'なし','2023-03-10 09:51:38'),(20,2,20,1,'なし','2023-03-10 09:51:38'),(21,2,21,1,'なし','2023-03-10 09:51:38'),(22,2,22,1,'なし','2023-03-10 09:51:38'),(23,2,23,1,'なし','2023-03-10 09:51:38'),(24,2,24,1,'なし','2023-03-10 09:51:38'),(25,2,25,1,'なし','2023-03-10 09:51:38'),(26,2,26,1,'なし','2023-03-10 09:51:38'),(27,2,27,1,'なし','2023-03-10 09:51:38'),(28,2,28,1,'なし','2023-03-10 09:51:38'),(29,2,29,1,'なし','2023-03-10 09:51:38'),(30,2,30,1,'なし','2023-03-10 09:51:38'),(31,1,1,5,'','2023-03-10 09:52:44'),(32,1,2,5,'','2023-03-10 09:52:44'),(33,1,3,5,'','2023-03-10 09:52:44'),(34,1,4,5,'','2023-03-10 09:52:44'),(35,1,5,5,'','2023-03-10 09:52:44'),(36,1,6,5,'','2023-03-10 09:52:44'),(37,1,7,5,'','2023-03-10 09:52:44'),(38,1,8,5,'','2023-03-10 09:52:44'),(39,1,9,5,'','2023-03-10 09:52:44'),(40,1,10,5,'','2023-03-10 09:52:44'),(41,1,11,5,'','2023-03-10 09:52:44'),(42,1,12,5,'','2023-03-10 09:52:44'),(43,1,13,5,'','2023-03-10 09:52:44'),(44,1,14,5,'','2023-03-10 09:52:44'),(45,1,15,5,'','2023-03-10 09:52:44'),(46,1,16,5,'','2023-03-10 09:52:44'),(47,1,17,5,'','2023-03-10 09:52:45'),(48,1,18,5,'','2023-03-10 09:52:45'),(49,1,19,5,'','2023-03-10 09:52:45'),(50,1,20,5,'','2023-03-10 09:52:45'),(51,1,21,5,'','2023-03-10 09:52:45'),(52,1,22,5,'','2023-03-10 09:52:45'),(53,1,23,5,'','2023-03-10 09:52:45'),(54,1,24,5,'','2023-03-10 09:52:45'),(55,1,25,5,'','2023-03-10 09:52:45'),(56,1,26,5,'','2023-03-10 09:52:45'),(57,1,27,5,'','2023-03-10 09:52:45'),(58,1,28,5,'','2023-03-10 09:52:45'),(59,1,29,5,'','2023-03-10 09:52:45'),(60,1,30,5,'','2023-03-10 09:52:45'),(61,1,1,8,'なし','2023-03-10 09:52:55'),(62,1,2,8,'なし','2023-03-10 09:52:55'),(63,1,3,8,'なし','2023-03-10 09:52:55'),(64,1,4,8,'なし','2023-03-10 09:52:55'),(65,1,5,8,'なし','2023-03-10 09:52:55'),(66,1,6,8,'なし','2023-03-10 09:52:55'),(67,1,7,8,'なし','2023-03-10 09:52:55'),(68,1,8,8,'なし','2023-03-10 09:52:55'),(69,1,9,8,'なし','2023-03-10 09:52:55'),(70,1,10,8,'なし','2023-03-10 09:52:55'),(71,1,11,8,'なし','2023-03-10 09:52:55'),(72,1,12,8,'なし','2023-03-10 09:52:55'),(73,1,13,8,'なし','2023-03-10 09:52:55'),(74,1,14,8,'なし','2023-03-10 09:52:55'),(75,1,15,8,'なし','2023-03-10 09:52:55'),(76,1,16,8,'なし','2023-03-10 09:52:55'),(77,1,17,8,'なし','2023-03-10 09:52:55'),(78,1,18,8,'なし','2023-03-10 09:52:55'),(79,1,19,8,'なし','2023-03-10 09:52:55'),(80,1,20,8,'なし','2023-03-10 09:52:55'),(81,1,21,8,'なし','2023-03-10 09:52:55'),(82,1,22,8,'なし','2023-03-10 09:52:55'),(83,1,23,8,'なし','2023-03-10 09:52:55'),(84,1,24,8,'なし','2023-03-10 09:52:55'),(85,1,25,8,'なし','2023-03-10 09:52:55'),(86,1,26,8,'なし','2023-03-10 09:52:55'),(87,1,27,8,'なし','2023-03-10 09:52:55'),(88,1,28,8,'なし','2023-03-10 09:52:55'),(89,1,29,8,'なし','2023-03-10 09:52:55'),(90,1,30,8,'なし','2023-03-10 09:52:55'),(91,1,1,2,'なし','2023-03-12 10:31:39'),(92,1,31,1,'なし','2023-03-12 10:37:54'),(93,1,31,3,'なし','2023-03-12 10:38:02'),(94,1,32,1,'なし','2023-03-12 14:58:16'),(95,1,33,1,'なし','2023-03-12 14:58:16'),(96,1,34,1,'なし','2023-03-12 14:58:16'),(97,1,35,1,'なし','2023-03-12 14:58:16'),(98,1,36,1,'なし','2023-03-12 14:58:16'),(99,1,32,5,'','2023-03-12 17:56:22'),(100,1,33,5,'','2023-03-12 17:56:23'),(101,2,37,1,'なし','2023-03-12 18:33:41'),(102,2,38,1,'なし','2023-03-12 18:33:41'),(103,2,39,1,'なし','2023-03-12 18:33:41'),(104,2,40,1,'なし','2023-03-12 18:33:41'),(105,2,41,1,'なし','2023-03-12 18:33:41'),(106,3,38,5,'','2023-03-12 18:41:57'),(107,4,30,9,'なし','2023-03-12 18:46:41'),(108,4,30,8,'なし','2023-03-12 18:49:13'),(109,3,34,6,'却下','2023-03-12 18:49:50'),(110,3,39,6,'却下','2023-03-12 18:50:55'),(111,2,39,6,'再提出のための編集','2023-03-12 18:56:13'),(112,2,13,2,'なし','2023-03-13 06:00:36'),(113,1,39,5,'','2023-03-13 08:30:22'),(114,1,35,5,'','2023-03-13 08:30:31'),(115,1,36,5,'','2023-03-13 08:30:31'),(116,1,32,8,'なし','2023-03-13 08:50:28'),(117,1,33,8,'なし','2023-03-13 08:50:28'),(118,1,35,8,'なし','2023-03-13 08:50:28'),(119,1,36,8,'なし','2023-03-13 08:50:28'),(120,1,38,8,'なし','2023-03-13 08:51:24'),(121,1,39,8,'なし','2023-03-13 08:55:31'),(122,1,42,1,'なし','2023-03-13 12:26:58'),(123,1,43,1,'なし','2023-03-13 12:26:58'),(124,1,44,1,'なし','2023-03-13 12:26:58'),(125,1,42,5,'','2023-03-13 17:01:07'),(126,1,43,5,'','2023-03-13 17:01:07'),(127,1,44,5,'','2023-03-13 17:01:07'),(128,2,45,1,'なし','2023-03-13 19:14:59'),(129,2,46,1,'なし','2023-03-13 19:14:59'),(130,1,34,5,'','2023-03-13 19:27:16'),(131,1,40,5,'','2023-03-13 19:28:43'),(132,1,41,5,'','2023-03-13 19:28:43'),(133,1,45,5,'','2023-03-13 19:28:43'),(134,1,46,5,'','2023-03-13 19:28:43'),(135,1,37,5,'','2023-03-13 19:28:43'),(136,1,34,8,'なし','2023-03-13 19:32:02'),(137,1,37,8,'なし','2023-03-13 19:32:02'),(138,1,40,8,'なし','2023-03-13 19:32:02'),(139,1,41,8,'なし','2023-03-13 19:32:02'),(140,1,42,8,'なし','2023-03-13 19:32:02'),(141,1,43,8,'なし','2023-03-13 19:32:02'),(142,1,44,8,'なし','2023-03-13 19:32:02'),(143,1,45,8,'なし','2023-03-13 19:32:02'),(144,1,46,8,'なし','2023-03-13 19:32:02'),(145,1,47,1,'なし','2023-03-13 19:36:33'),(146,1,48,1,'なし','2023-03-13 19:36:33'),(147,1,49,1,'なし','2023-03-13 19:36:33'),(148,1,50,1,'なし','2023-03-13 19:36:33'),(149,1,51,1,'なし','2023-03-13 19:36:33'),(150,1,47,6,'却下','2023-03-13 19:36:52'),(151,1,47,5,'OK','2023-03-13 19:39:23'),(152,1,48,6,'却下','2023-03-13 19:39:40'),(153,1,48,5,'おk','2023-03-13 19:40:23'),(154,1,15,2,'なし','2023-03-13 19:54:03'),(155,1,15,2,'なし','2023-03-13 19:54:37');
/*!40000 ALTER TABLE `record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requested_question`
--

DROP TABLE IF EXISTS `requested_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requested_question` (
  `id` int NOT NULL AUTO_INCREMENT,
  `request_id` int DEFAULT NULL,
  `question` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `request_id` (`request_id`),
  KEY `question` (`question`),
  CONSTRAINT `requested_question_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `question_request` (`id`) ON DELETE CASCADE,
  CONSTRAINT `requested_question_ibfk_2` FOREIGN KEY (`question`) REFERENCES `question` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requested_question`
--

LOCK TABLES `requested_question` WRITE;
/*!40000 ALTER TABLE `requested_question` DISABLE KEYS */;
INSERT INTO `requested_question` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28),(29,1,29),(30,1,30),(31,2,32),(32,2,33),(33,3,34),(34,4,37),(35,5,38),(36,6,39),(37,7,39),(38,8,35),(39,8,36),(40,9,42),(41,9,43),(42,9,44),(43,10,34),(44,11,40),(45,11,41),(46,11,45),(47,11,46),(48,11,37),(49,12,47),(50,13,47),(51,14,48),(52,15,48);
/*!40000 ALTER TABLE `requested_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `score`
--

DROP TABLE IF EXISTS `score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `score` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` int DEFAULT NULL,
  `question` int DEFAULT NULL,
  `correct` tinyint(1) NOT NULL,
  `review` tinyint(1) NOT NULL,
  `answered_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user` (`user`),
  KEY `question` (`question`),
  CONSTRAINT `score_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `score_ibfk_2` FOREIGN KEY (`question`) REFERENCES `question` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=162 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `score`
--

LOCK TABLES `score` WRITE;
/*!40000 ALTER TABLE `score` DISABLE KEYS */;
INSERT INTO `score` VALUES (1,1,1,1,0,'2023-03-10 09:53:02'),(2,1,2,1,0,'2023-03-10 09:53:03'),(3,1,3,1,0,'2023-03-10 09:53:04'),(4,1,4,1,0,'2023-03-10 09:53:05'),(5,1,5,1,0,'2023-03-10 09:53:05'),(6,1,6,1,0,'2023-03-10 09:53:29'),(7,1,7,1,0,'2023-03-10 09:53:30'),(8,1,8,1,0,'2023-03-10 09:53:31'),(9,1,9,1,0,'2023-03-10 09:53:32'),(10,1,10,1,0,'2023-03-10 09:53:33'),(11,1,1,0,0,'2023-03-10 09:54:09'),(12,1,2,1,0,'2023-03-10 09:54:10'),(13,1,3,1,0,'2023-03-10 09:54:11'),(14,1,4,1,0,'2023-03-10 09:54:12'),(15,1,5,1,0,'2023-03-10 09:54:12'),(16,1,1,1,0,'2023-03-10 09:54:28'),(17,1,6,0,0,'2023-03-10 09:54:33'),(18,1,7,1,0,'2023-03-10 09:54:34'),(19,1,8,1,0,'2023-03-10 09:54:34'),(20,1,9,1,0,'2023-03-10 09:54:35'),(21,1,10,1,0,'2023-03-10 09:54:36'),(22,1,11,0,0,'2023-03-10 09:54:38'),(23,1,12,1,0,'2023-03-10 09:54:39'),(24,1,13,1,0,'2023-03-10 09:54:40'),(25,1,14,1,0,'2023-03-10 09:54:40'),(26,1,15,1,0,'2023-03-10 09:54:41'),(27,1,11,1,0,'2023-03-10 09:54:56'),(28,1,16,0,0,'2023-03-10 10:11:50'),(29,1,17,0,0,'2023-03-10 10:11:51'),(30,1,18,1,0,'2023-03-10 10:11:52'),(31,1,19,0,0,'2023-03-10 10:11:52'),(32,1,20,0,0,'2023-03-10 10:11:53'),(33,1,16,1,0,'2023-03-10 10:11:56'),(34,1,17,0,0,'2023-03-10 10:11:56'),(35,1,19,1,0,'2023-03-10 10:11:57'),(36,1,20,0,0,'2023-03-10 10:11:58'),(37,1,6,0,0,'2023-03-10 10:14:18'),(38,1,17,1,0,'2023-03-10 10:14:19'),(39,1,20,0,0,'2023-03-10 10:14:20'),(40,1,20,0,0,'2023-03-10 10:17:08'),(41,1,6,0,0,'2023-03-10 10:17:09'),(42,1,20,1,0,'2023-03-10 10:17:18'),(43,1,6,1,0,'2023-03-10 10:17:18'),(44,1,21,1,0,'2023-03-10 10:24:48'),(45,1,22,0,0,'2023-03-10 10:24:50'),(46,1,22,0,0,'2023-03-10 10:24:57'),(47,1,23,0,0,'2023-03-10 10:25:09'),(48,1,24,0,0,'2023-03-10 10:25:09'),(49,1,25,0,0,'2023-03-10 10:25:10'),(50,1,26,1,0,'2023-03-10 10:25:15'),(51,1,27,0,0,'2023-03-10 10:25:16'),(52,1,28,1,0,'2023-03-10 10:25:16'),(53,1,29,1,0,'2023-03-10 10:25:17'),(54,1,30,0,0,'2023-03-10 10:25:17'),(55,1,27,0,0,'2023-03-10 10:25:20'),(56,1,30,1,0,'2023-03-10 10:25:21'),(57,1,27,0,0,'2023-03-10 10:25:23'),(58,1,26,1,0,'2023-03-10 10:25:33'),(59,1,28,1,0,'2023-03-10 10:25:34'),(60,1,29,1,0,'2023-03-10 10:25:35'),(61,1,30,0,0,'2023-03-10 10:25:36'),(62,1,27,1,0,'2023-03-10 10:25:37'),(63,1,23,0,0,'2023-03-10 10:25:43'),(64,1,22,1,0,'2023-03-10 10:25:44'),(65,1,25,1,0,'2023-03-10 10:25:44'),(66,1,24,0,0,'2023-03-10 10:25:45'),(67,1,30,1,0,'2023-03-10 10:25:46'),(68,1,24,1,0,'2023-03-10 10:28:41'),(69,1,23,0,0,'2023-03-10 10:28:42'),(70,1,2,0,0,'2023-03-10 10:35:14'),(71,1,3,0,0,'2023-03-10 10:35:15'),(72,1,4,0,0,'2023-03-10 10:35:16'),(73,1,5,0,0,'2023-03-10 10:35:16'),(74,1,1,0,0,'2023-03-10 10:35:17'),(75,1,7,0,0,'2023-03-10 10:35:20'),(76,1,8,0,0,'2023-03-10 10:35:21'),(77,1,9,0,0,'2023-03-10 10:35:21'),(78,1,10,0,0,'2023-03-10 10:35:22'),(79,1,6,0,0,'2023-03-10 10:35:23'),(80,1,4,0,0,'2023-03-10 10:43:56'),(81,1,6,1,0,'2023-03-10 10:43:58'),(82,1,3,0,0,'2023-03-10 10:43:59'),(83,1,1,1,0,'2023-03-10 10:44:00'),(84,1,2,0,0,'2023-03-10 10:44:03'),(85,1,7,1,0,'2023-03-10 10:44:05'),(86,1,10,0,0,'2023-03-10 10:44:06'),(87,1,23,1,0,'2023-03-10 10:47:29'),(88,1,5,0,0,'2023-03-10 10:47:30'),(89,1,10,1,0,'2023-03-10 10:47:31'),(90,1,2,0,0,'2023-03-10 10:47:31'),(91,1,9,1,0,'2023-03-10 10:47:32'),(92,1,2,0,0,'2023-03-10 16:44:51'),(93,1,4,1,0,'2023-03-10 16:44:52'),(94,1,8,1,0,'2023-03-10 16:44:53'),(95,1,3,0,0,'2023-03-11 14:25:14'),(96,1,5,1,0,'2023-03-11 14:25:29'),(97,1,1,0,0,'2023-03-11 14:26:51'),(98,1,4,0,0,'2023-03-11 14:27:28'),(99,1,2,1,0,'2023-03-11 14:28:59'),(100,1,7,1,0,'2023-03-11 14:29:29'),(101,1,8,1,0,'2023-03-11 14:29:30'),(102,1,9,0,0,'2023-03-11 14:29:43'),(103,1,10,0,0,'2023-03-11 14:29:44'),(104,1,6,0,0,'2023-03-11 14:29:45'),(105,1,12,1,0,'2023-03-11 14:30:08'),(106,1,13,1,0,'2023-03-11 14:30:10'),(107,1,14,0,0,'2023-03-11 14:30:13'),(108,1,15,1,0,'2023-03-11 14:30:15'),(109,1,11,0,0,'2023-03-11 14:30:16'),(110,1,6,1,0,'2023-03-11 14:30:43'),(111,1,4,0,0,'2023-03-11 14:30:45'),(112,1,11,1,0,'2023-03-11 14:30:48'),(113,1,9,0,0,'2023-03-11 14:30:51'),(114,1,14,0,0,'2023-03-11 14:30:55'),(115,1,14,0,0,'2023-03-11 18:23:38'),(116,1,1,1,0,'2023-03-11 18:23:39'),(117,1,9,1,0,'2023-03-11 18:23:40'),(118,1,3,1,0,'2023-03-11 18:23:42'),(119,1,10,1,0,'2023-03-11 18:23:43'),(120,1,21,0,0,'2023-03-11 18:35:38'),(121,1,25,1,0,'2023-03-11 18:35:40'),(122,1,22,0,0,'2023-03-11 18:35:41'),(123,1,24,1,0,'2023-03-11 18:35:43'),(124,1,23,0,0,'2023-03-11 18:35:48'),(125,1,26,0,0,'2023-03-11 18:36:07'),(126,1,28,1,0,'2023-03-11 18:36:08'),(127,1,29,0,0,'2023-03-11 18:36:11'),(128,2,11,1,0,'2023-03-13 05:59:48'),(129,2,12,0,0,'2023-03-13 06:00:05'),(130,2,13,0,0,'2023-03-13 06:00:41'),(131,2,14,0,0,'2023-03-13 06:00:51'),(132,2,15,1,0,'2023-03-13 06:01:02'),(133,2,12,1,0,'2023-03-13 06:01:19'),(134,2,13,1,0,'2023-03-13 06:01:28'),(135,2,14,1,0,'2023-03-13 06:01:37'),(136,1,32,1,0,'2023-03-13 09:00:15'),(137,1,33,1,0,'2023-03-13 09:00:22'),(138,1,35,1,0,'2023-03-13 09:00:27'),(139,1,36,1,0,'2023-03-13 09:00:35'),(140,1,38,0,0,'2023-03-13 09:00:58'),(141,1,39,1,0,'2023-03-13 09:01:10'),(142,1,21,1,0,'2023-03-13 17:00:09'),(143,6,1,1,0,'2023-03-13 17:04:43'),(144,6,2,0,0,'2023-03-13 17:04:48'),(145,6,3,1,0,'2023-03-13 17:05:06'),(146,6,4,1,0,'2023-03-13 17:05:08'),(147,6,5,0,0,'2023-03-13 17:05:09'),(148,6,6,1,0,'2023-03-13 17:05:16'),(149,6,7,0,0,'2023-03-13 17:05:17'),(150,6,8,0,0,'2023-03-13 17:05:36'),(151,6,9,1,0,'2023-03-13 17:05:38'),(152,6,10,1,0,'2023-03-13 17:06:23'),(153,6,1,1,0,'2023-03-13 17:24:04'),(154,6,2,0,0,'2023-03-13 17:24:11'),(155,1,29,1,0,'2023-03-18 17:07:24'),(156,1,23,1,0,'2023-03-18 17:07:31'),(157,1,26,1,0,'2023-03-18 17:07:35'),(158,1,38,1,0,'2023-03-18 17:07:40'),(159,1,22,1,0,'2023-03-18 17:07:49'),(160,1,14,1,0,'2023-03-18 17:08:03'),(161,1,4,1,0,'2023-03-18 17:08:05');
/*!40000 ALTER TABLE `score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `style`
--

DROP TABLE IF EXISTS `style`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `style` (
  `id` int NOT NULL AUTO_INCREMENT,
  `style` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `style`
--

LOCK TABLES `style` WRITE;
/*!40000 ALTER TABLE `style` DISABLE KEYS */;
INSERT INTO `style` VALUES (1,'ハムニダ体'),(2,'ヘヨ体'),(3,'ヘ体'),(4,'ハンダ体'),(5,'ハオ体');
/*!40000 ALTER TABLE `style` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `target_grade` int NOT NULL,
  `edit` tinyint(1) NOT NULL,
  `check` tinyint(1) NOT NULL,
  `approve` tinyint(1) NOT NULL,
  `admin` tinyint(1) NOT NULL,
  `registered_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `target_grade` (`target_grade`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`target_grade`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'test','test@test.com','sha256$T4YifZqw7C2RWafJ$d4b1cc2a85e224d1171ac54a532ef6abd0183fbd52542268ff7f8a53f251b6fa',1,1,1,1,1,'2023-03-10 09:50:35'),(2,'editor','editor@test.com','sha256$vqJmE2u0n2JdfRIY$de883570982838ed1ec74000dea0f1ba9ccb7e81e7ed378c1c422c0c2360e42d',1,1,0,0,0,'2023-03-10 09:50:35'),(3,'checker','checker@test.com','sha256$i598Pi0geiXxuvaK$c5f8081853a323644f80c57e9302a8a05744ed56ea392d8136d469a54c098158',1,0,1,0,0,'2023-03-10 09:50:35'),(4,'approver','approver@test.com','sha256$IiZO7LFtigz98lG5$20f0f79365a017fe13dcce9730ef86c6186febd051f365f98390d8138df40032',1,0,0,1,0,'2023-03-10 09:50:35'),(5,'yuri','yuri@yuri.com','sha256$5skK46LBdjgzlVsk$f59e3edbb1cb1af1e7272253d023e5133510519117a44b333d591ad781fee979',1,0,0,0,0,'2023-03-13 05:15:02'),(6,NULL,NULL,'sha256$ZFonHHoAukNltd96$0b3f31eea398a97ab59a8fc7827f1096035770d811ca42cff828770e82a823f2',1,0,0,0,0,'2023-03-13 17:03:41'),(7,'test3','test3@test.com','sha256$EmqY149groPUUl2D$26707da2843d288871828111b299181ef6666825ceeb50a08451b16aafafdb53',1,0,0,0,0,'2023-03-13 17:04:22'),(8,NULL,NULL,'sha256$Hgh4HbaGN0nYANXD$f35c622f1b6dd55f1788af29d65a2fb94ff6e18dfa4c3ac07d5a39798cc2b9c6',1,1,0,0,0,'2023-03-14 10:29:10'),(9,'サクッと作子','saku@sakusaku.com','sha256$VE8Xz37dGYO1gBcz$21c92706a044f3b9048f718a93d5bdaf6011fac743928e0e37e8074d94404984',1,0,0,0,0,'2023-03-16 14:52:08'),(10,'サクッと作文','saku2@sakusaku.com','sha256$GtzB4N9HqvvzlamM$32226ef83fdc278983395e54544608bbaaf347f4d849a4b65be69898d370ba8b',1,0,0,0,0,'2023-03-16 14:53:58');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `word`
--

DROP TABLE IF EXISTS `word`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `word` (
  `id` int NOT NULL AUTO_INCREMENT,
  `japanese` varchar(100) DEFAULT NULL,
  `foreign_l` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `word`
--

LOCK TABLES `word` WRITE;
/*!40000 ALTER TABLE `word` DISABLE KEYS */;
INSERT INTO `word` VALUES (2,'医者','의사'),(3,'学生','학생'),(4,'母','어머니'),(5,'公務員','공무원'),(6,'カバン','가방'),(7,'これ','이것'),(8,'キムチ','김치'),(9,'今日','오늘'),(10,'休日','휴일'),(11,'ここ','여기'),(12,'銀行','은행'),(13,'風邪','감기'),(14,'ノート','노트'),(15,'弟','남동생'),(16,'宿題','숙제'),(17,'火曜日','화요일'),(18,'父','아버지'),(19,'試験','시험'),(20,'姉','언니'),(21,'妹','여동생'),(22,'日曜日','일요일'),(23,'授業','수업'),(24,'家','집'),(25,'月','월'),(26,'日','일'),(27,'誕生日','생일'),(28,'コンピューター','컴퓨터'),(29,'は','는'),(30,'である','이다');
/*!40000 ALTER TABLE `word` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-19  0:54:54
