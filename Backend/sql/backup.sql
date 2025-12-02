-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: iso_tank
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `cargo_tank_master`
--

DROP TABLE IF EXISTS `cargo_tank_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cargo_tank_master` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cargo_reference` varchar(100) NOT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_cargo_tank_master_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargo_tank_master`
--

LOCK TABLES `cargo_tank_master` WRITE;
/*!40000 ALTER TABLE `cargo_tank_master` DISABLE KEYS */;
INSERT INTO `cargo_tank_master` VALUES (1,'CT-Alpha-01',NULL,NULL,'2025-11-28 15:07:19','2025-11-28 15:07:19'),(2,'CT-Bravo-02',NULL,NULL,'2025-11-28 15:07:19','2025-11-28 15:07:19'),(3,'LNG-Storage-05',NULL,NULL,'2025-11-28 15:07:19','2025-11-28 15:07:19'),(4,'LPG-Transport-09',NULL,NULL,'2025-11-28 15:07:19','2025-11-28 15:07:19'),(5,'Chem-Residue-X1',NULL,NULL,'2025-11-28 15:07:19','2025-11-28 15:07:19');
/*!40000 ALTER TABLE `cargo_tank_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cargo_tank_transaction`
--

DROP TABLE IF EXISTS `cargo_tank_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cargo_tank_transaction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tank_id` int NOT NULL,
  `cargo_reference` int NOT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL,
  `density` varchar(100) DEFAULT NULL,
  `compatability_notes` varchar(500) DEFAULT NULL,
  `cargo_master_id` int DEFAULT NULL,
  `loading_parts` varchar(500) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `tank_id` (`tank_id`),
  KEY `cargo_reference` (`cargo_reference`),
  KEY `cargo_master_id` (`cargo_master_id`),
  KEY `ix_cargo_tank_transaction_id` (`id`),
  CONSTRAINT `cargo_tank_transaction_ibfk_1` FOREIGN KEY (`tank_id`) REFERENCES `tank_details` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cargo_tank_transaction_ibfk_2` FOREIGN KEY (`cargo_reference`) REFERENCES `cargo_tank_master` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cargo_tank_transaction_ibfk_3` FOREIGN KEY (`cargo_master_id`) REFERENCES `cargo_tank_master` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargo_tank_transaction`
--

LOCK TABLES `cargo_tank_transaction` WRITE;
/*!40000 ALTER TABLE `cargo_tank_transaction` DISABLE KEYS */;
INSERT INTO `cargo_tank_transaction` VALUES (1,1,1,'Admin',NULL,'1.1kg/m^3','teflon',1,'valve','2025-11-28 15:08:45','2025-11-28 15:08:45'),(2,1,2,'Admin',NULL,'1.5kg/m^3','Requires teflon',2,'pump valve 1','2025-11-29 04:05:06','2025-11-29 04:05:06');
/*!40000 ALTER TABLE `cargo_tank_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `checklist_master`
--

DROP TABLE IF EXISTS `checklist_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `checklist_master` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `sub_job_id` int NOT NULL,
  `sn` varchar(16) NOT NULL,
  `sub_job_name` varchar(255) NOT NULL,
  `sub_job_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_checklist_master_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `checklist_master`
--

LOCK TABLES `checklist_master` WRITE;
/*!40000 ALTER TABLE `checklist_master` DISABLE KEYS */;
/*!40000 ALTER TABLE `checklist_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_type`
--

DROP TABLE IF EXISTS `image_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image_type` varchar(100) NOT NULL,
  `description` text,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  `count` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_type`
--

LOCK TABLES `image_type` WRITE;
/*!40000 ALTER TABLE `image_type` DISABLE KEYS */;
INSERT INTO `image_type` VALUES (1,'Front View','General tank photos','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(2,'Rear View','Photos from rear side','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(3,'Top View','Photos from top','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(4,'Underside View 01','Underside photo #1','2025-11-28 17:01:26','2025-11-28 17:01:26',1),(5,'Front LH View','Left-hand front view','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(6,'Rear LH View','Left-hand rear view','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(7,'Front RH View','Right-hand front view','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(8,'Rear RH View','Right-hand rear view','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(9,'LH Side View','Left side view','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(10,'RH Side View','Right side view','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(11,'Valves Section View','Valves section photos','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(12,'Safety Valve','Safety valve photos','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(13,'Level / Pressure Gauge','Photos showing gauge readings','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(14,'Vacuum Reading','Vacuum reading photos','2025-11-26 20:55:29','2025-11-26 20:55:29',1),(15,'Underside View 02','Underside photo #2','2025-11-28 17:01:26','2025-11-28 17:01:26',1);
/*!40000 ALTER TABLE `image_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inspection_checklist`
--

DROP TABLE IF EXISTS `inspection_checklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspection_checklist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `inspection_id` int NOT NULL,
  `tank_id` int DEFAULT NULL,
  `emp_id` int DEFAULT NULL,
  `job_id` int DEFAULT NULL,
  `job_name` varchar(255) DEFAULT NULL,
  `sub_job_id` int DEFAULT NULL,
  `sn` varchar(16) NOT NULL,
  `sub_job_description` varchar(512) DEFAULT NULL,
  `status_id` int NOT NULL,
  `status` varchar(32) DEFAULT NULL,
  `comment` text,
  `flagged` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_inspection_checklist_tank_id` (`tank_id`),
  KEY `ix_inspection_checklist_inspection_id` (`inspection_id`),
  KEY `ix_inspection_checklist_emp_id` (`emp_id`),
  CONSTRAINT `inspection_checklist_ibfk_1` FOREIGN KEY (`inspection_id`) REFERENCES `tank_inspection_details` (`inspection_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inspection_checklist`
--

LOCK TABLES `inspection_checklist` WRITE;
/*!40000 ALTER TABLE `inspection_checklist` DISABLE KEYS */;
INSERT INTO `inspection_checklist` VALUES (10,2,1,1001,4,'Valves Tightness & Operation',20,'4.3','Valve Tightness Incl Glands',1,'Fail','fixed issue',0,'2025-11-28 15:35:30','2025-11-29 22:12:06');
/*!40000 ALTER TABLE `inspection_checklist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inspection_job`
--

DROP TABLE IF EXISTS `inspection_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspection_job` (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `job_code` varchar(32) DEFAULT NULL,
  `job_description` varchar(255) NOT NULL,
  `sort_order` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inspection_job`
--

LOCK TABLES `inspection_job` WRITE;
/*!40000 ALTER TABLE `inspection_job` DISABLE KEYS */;
INSERT INTO `inspection_job` VALUES (1,'BODY','Tank Body & Frame Condition',1,'2025-11-28 12:05:46',NULL),(2,'PIPE','Pipework & Installation',2,'2025-11-28 12:05:46',NULL),(3,'INSTR','Tank Instrument & Assembly',3,'2025-11-28 12:05:46',NULL),(4,'VALVE','Valves Tightness & Operation',4,'2025-11-28 12:05:46',NULL),(5,'DEPART','Before Departure Check',5,'2025-11-28 12:05:46',NULL),(6,'OTHER','Others Observation & Comment',6,'2025-11-28 12:05:46',NULL);
/*!40000 ALTER TABLE `inspection_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inspection_status`
--

DROP TABLE IF EXISTS `inspection_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspection_status` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `status_name` varchar(32) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `sort_order` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`status_id`),
  UNIQUE KEY `status_name` (`status_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inspection_status`
--

LOCK TABLES `inspection_status` WRITE;
/*!40000 ALTER TABLE `inspection_status` DISABLE KEYS */;
INSERT INTO `inspection_status` VALUES (1,'OK','Inspection passed',NULL,NULL,NULL),(2,'Faulty','Requires attention or repair',NULL,NULL,NULL),(3,'Not Inspected','Not yet inspected',NULL,NULL,NULL);
/*!40000 ALTER TABLE `inspection_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inspection_sub_job`
--

DROP TABLE IF EXISTS `inspection_sub_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspection_sub_job` (
  `sub_job_id` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `sn` varchar(16) NOT NULL,
  `sub_job_description` varchar(512) NOT NULL,
  `sort_order` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`sub_job_id`),
  UNIQUE KEY `sn` (`sn`),
  KEY `job_id` (`job_id`),
  CONSTRAINT `inspection_sub_job_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `inspection_job` (`job_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inspection_sub_job`
--

LOCK TABLES `inspection_sub_job` WRITE;
/*!40000 ALTER TABLE `inspection_sub_job` DISABLE KEYS */;
INSERT INTO `inspection_sub_job` VALUES (1,1,'1.1','Body x 6 Sides & All Frame – No Dent / No Bent / No Deep Cut',1,'2025-11-28 12:07:18',NULL),(2,1,'1.2','Cabin Door & Frame Condition – No Damage / Can Lock',2,'2025-11-28 12:07:18',NULL),(3,1,'1.3','Tank Number, Product & Hazchem Label – Not Missing or Tear',3,'2025-11-28 12:07:18',NULL),(4,1,'1.4','Condition of Paint Work & Cleanliness – Clean / No Bad Rust',4,'2025-11-28 12:07:18',NULL),(5,1,'1.5','Others',5,'2025-11-28 12:07:18',NULL),(6,2,'2.1','Pipework Supports / Brackets – Not Loose / No Bent',1,'2025-11-28 12:07:18',NULL),(7,2,'2.2','Pipework Joint & Welding – No Crack / No Icing / No Leaking',2,'2025-11-28 12:07:18',NULL),(8,2,'2.3','Earthing Point',3,'2025-11-28 12:07:18',NULL),(9,2,'2.4','PBU Support & Flange Connection – No Leak / Not Damage',4,'2025-11-28 12:07:18',NULL),(10,2,'2.5','Others',5,'2025-11-28 12:07:18',NULL),(11,3,'3.1','Safety Diverter Valve – Switching Lever',1,'2025-11-28 12:07:18',NULL),(12,3,'3.2','Safety Valves Connection & Joint – No Leaks',2,'2025-11-28 12:07:18',NULL),(13,3,'3.3','Level & Pressure Gauge Support Bracket, Connection & Joint – Not Loosen / No Leaks',3,'2025-11-28 12:07:18',NULL),(14,3,'3.4','Level & Pressure Gauge – Function Check',4,'2025-11-28 12:07:18',NULL),(15,3,'3.5','Level & Pressure Gauge Valve Open / Balance Valve Close',5,'2025-11-28 12:07:18',NULL),(16,3,'3.6','Data & CSC Plate – Not Missing / Not Damage',6,'2025-11-28 12:07:18',NULL),(17,3,'3.7','Others',7,'2025-11-28 12:07:18',NULL),(18,4,'4.1','Valve Handwheel – Not Missing / Nut Not Loose',1,'2025-11-28 12:07:18',NULL),(19,4,'4.2','Valve Open & Close Operation – No Seizing / Not Tight / Not Jam',2,'2025-11-28 12:07:18',NULL),(20,4,'4.3','Valve Tightness Incl Glands – No Leak / No Icing / No Passing',3,'2025-11-28 12:07:18',NULL),(21,4,'4.4','Anchor Point',4,'2025-11-28 12:07:18',NULL),(22,4,'4.5','Others',5,'2025-11-28 12:07:18',NULL),(23,5,'5.1','All Valves Closed – Defrost & Close Firmly',1,'2025-11-28 12:07:18',NULL),(24,5,'5.2','Caps fitted to Outlets or Cover from Dust if applicable',2,'2025-11-28 12:07:18',NULL),(25,5,'5.3','Security Seal Fitted by Refilling Plant - Check',3,'2025-11-28 12:07:18',NULL),(26,5,'5.4','Pressure Gauge – lowest possible',4,'2025-11-28 12:07:18',NULL),(27,5,'5.5','Level Gauge – Within marking or standard indication',5,'2025-11-28 12:07:18',NULL),(28,5,'5.6','Weight Reading – ensure within acceptance weight',6,'2025-11-28 12:07:18',NULL),(29,5,'5.7','Cabin Door Lock – Secure and prevent from sudden opening',7,'2025-11-28 12:07:18',NULL),(30,5,'5.8','Others',8,'2025-11-28 12:07:18',NULL);
/*!40000 ALTER TABLE `inspection_sub_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inspection_type`
--

DROP TABLE IF EXISTS `inspection_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inspection_type` (
  `inspection_type_id` int NOT NULL AUTO_INCREMENT,
  `inspection_type_name` varchar(150) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`inspection_type_id`),
  UNIQUE KEY `inspection_type_name` (`inspection_type_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inspection_type`
--

LOCK TABLES `inspection_type` WRITE;
/*!40000 ALTER TABLE `inspection_type` DISABLE KEYS */;
INSERT INTO `inspection_type` VALUES (1,'Incoming','Incoming inspection',NULL,NULL),(2,'Outgoing','Outgoing inspection',NULL,NULL),(3,'On-Hire','On-hire inspection',NULL,NULL),(4,'Off-Hire','Off-hire inspection',NULL,NULL),(5,'Condition','Condition check',NULL,NULL);
/*!40000 ALTER TABLE `inspection_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location_master`
--

DROP TABLE IF EXISTS `location_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location_master` (
  `location_id` int NOT NULL AUTO_INCREMENT,
  `location_name` varchar(255) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location_master`
--

LOCK TABLES `location_master` WRITE;
/*!40000 ALTER TABLE `location_master` DISABLE KEYS */;
INSERT INTO `location_master` VALUES (1,'SG-1 16A, Benoi Cresent','Default location',NULL,NULL),(2,'SG-2 5A Jalan Papan','Alternate location',NULL,NULL),(3,'China QD','China QD location',NULL,NULL);
/*!40000 ALTER TABLE `location_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_session`
--

DROP TABLE IF EXISTS `login_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_session` (
  `id` int NOT NULL AUTO_INCREMENT,
  `emp_id` int NOT NULL,
  `token` varchar(500) DEFAULT NULL,
  `still_logged_in` int DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_session`
--

LOCK TABLES `login_session` WRITE;
/*!40000 ALTER TABLE `login_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `login_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_sessions`
--

DROP TABLE IF EXISTS `login_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `emp_id` int NOT NULL,
  `email` varchar(255) NOT NULL,
  `logged_in_at` timestamp NULL DEFAULT (now()),
  `still_logged_in` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `emp_id` (`emp_id`),
  KEY `ix_login_sessions_id` (`id`),
  CONSTRAINT `login_sessions_ibfk_1` FOREIGN KEY (`emp_id`) REFERENCES `users` (`emp_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_sessions`
--

LOCK TABLES `login_sessions` WRITE;
/*!40000 ALTER TABLE `login_sessions` DISABLE KEYS */;
INSERT INTO `login_sessions` VALUES (1,1001,'naveen@gmail.com','2025-11-27 14:14:47',1);
/*!40000 ALTER TABLE `login_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operators`
--

DROP TABLE IF EXISTS `operators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operators` (
  `id` int NOT NULL AUTO_INCREMENT,
  `operator_id` int NOT NULL,
  `operator_name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  `updated_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_operators_operator_id` (`operator_id`),
  CONSTRAINT `operators_ibfk_1` FOREIGN KEY (`operator_id`) REFERENCES `users` (`emp_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operators`
--

LOCK TABLES `operators` WRITE;
/*!40000 ALTER TABLE `operators` DISABLE KEYS */;
INSERT INTO `operators` VALUES (2,1001,'naveen','2025-11-28 23:49:46','2025-11-28 23:49:46');
/*!40000 ALTER TABLE `operators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_master`
--

DROP TABLE IF EXISTS `product_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_master` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(150) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `product_name` (`product_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_master`
--

LOCK TABLES `product_master` WRITE;
/*!40000 ALTER TABLE `product_master` DISABLE KEYS */;
INSERT INTO `product_master` VALUES (1,'Liquid Argon','Cryogenic product - Liquid Argon',NULL,NULL),(2,'Liquid Carbon Dioxide','Cryogenic product - Liquid CO2',NULL,NULL),(3,'Liquid Oxygen','Cryogenic product - Liquid O2',NULL,NULL),(4,'Liquid Nitrogen','Cryogenic product - Liquid N2',NULL,NULL),(5,'Others','Other product - specified in notes',NULL,NULL);
/*!40000 ALTER TABLE `product_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `regulations_master`
--

DROP TABLE IF EXISTS `regulations_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regulations_master` (
  `id` int NOT NULL AUTO_INCREMENT,
  `regulation_name` varchar(100) NOT NULL,
  `created_by` int DEFAULT NULL,
  `updated_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `regulation_name` (`regulation_name`),
  KEY `ix_regulations_master_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regulations_master`
--

LOCK TABLES `regulations_master` WRITE;
/*!40000 ALTER TABLE `regulations_master` DISABLE KEYS */;
INSERT INTO `regulations_master` VALUES (1,'API Standard 650',NULL,NULL,'2025-11-28 20:37:19','2025-11-28 20:37:19'),(2,'ISO 9001:2015',NULL,NULL,'2025-11-28 20:37:19','2025-11-28 20:37:19'),(3,'OSHA 1910.119',NULL,NULL,'2025-11-28 20:37:19','2025-11-28 20:37:19'),(4,'MARPOL Annex I',NULL,NULL,'2025-11-28 20:37:19','2025-11-28 20:37:19'),(5,'ASME Section VIII',NULL,NULL,'2025-11-28 20:37:19','2025-11-28 20:37:19');
/*!40000 ALTER TABLE `regulations_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `safety_valve_brand`
--

DROP TABLE IF EXISTS `safety_valve_brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `safety_valve_brand` (
  `id` int NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(255) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `brand_name` (`brand_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `safety_valve_brand`
--

LOCK TABLES `safety_valve_brand` WRITE;
/*!40000 ALTER TABLE `safety_valve_brand` DISABLE KEYS */;
INSERT INTO `safety_valve_brand` VALUES (1,'Generic Brand','Generic safety valves',NULL,NULL),(2,'Fisher','Fisher safety valves',NULL,NULL),(3,'TESCOM','TESCOM safety valves',NULL,NULL),(4,'Bonomi','Bonomi safety valves',NULL,NULL),(5,'Other','Other brands',NULL,NULL);
/*!40000 ALTER TABLE `safety_valve_brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `safety_valve_model`
--

DROP TABLE IF EXISTS `safety_valve_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `safety_valve_model` (
  `id` int NOT NULL AUTO_INCREMENT,
  `model_name` varchar(255) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `model_name` (`model_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `safety_valve_model`
--

LOCK TABLES `safety_valve_model` WRITE;
/*!40000 ALTER TABLE `safety_valve_model` DISABLE KEYS */;
INSERT INTO `safety_valve_model` VALUES (1,'Superflow 3','Fort Vale - Standard Relief Valve','2025-11-29 18:49:58','2025-11-29 18:49:58'),(2,'Perolo ATCO','Perolo - Standard 2.5 inch Valve','2025-11-29 18:49:58','2025-11-29 18:49:58'),(3,'Cleanflow','Fort Vale - Hygienic/Food Grade','2025-11-29 18:49:58','2025-11-29 18:49:58'),(4,'Perolo 3.0','Perolo - High Flow 3 inch','2025-11-29 18:49:58','2025-11-29 18:49:58');
/*!40000 ALTER TABLE `safety_valve_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `safety_valve_size`
--

DROP TABLE IF EXISTS `safety_valve_size`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `safety_valve_size` (
  `id` int NOT NULL AUTO_INCREMENT,
  `size_label` varchar(255) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `size_label` (`size_label`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `safety_valve_size`
--

LOCK TABLES `safety_valve_size` WRITE;
/*!40000 ALTER TABLE `safety_valve_size` DISABLE KEYS */;
INSERT INTO `safety_valve_size` VALUES (1,'2.5 Inch','Standard ISO Tank Size','2025-11-29 18:49:04','2025-11-29 18:49:04'),(2,'3 Inch','High Flow / Gas Tank Size','2025-11-29 18:49:04','2025-11-29 18:49:04'),(3,'DN 80','Metric Equivalent (80mm)','2025-11-29 18:49:04','2025-11-29 18:49:04'),(4,'DN 65','Metric Equivalent (65mm)','2025-11-29 18:49:04','2025-11-29 18:49:04');
/*!40000 ALTER TABLE `safety_valve_size` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank_certificate`
--

DROP TABLE IF EXISTS `tank_certificate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_certificate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tank_id` int NOT NULL,
  `tank_number` varchar(50) NOT NULL,
  `year_of_manufacturing` varchar(10) DEFAULT NULL,
  `insp_2_5y_date` date DEFAULT NULL,
  `next_insp_date` date DEFAULT NULL,
  `inspection_agency` varchar(10) DEFAULT NULL,
  `certificate_number` varchar(255) NOT NULL,
  `certificate_file` varchar(255) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `certificate_number` (`certificate_number`),
  KEY `tank_id` (`tank_id`),
  KEY `ix_tank_certificate_id` (`id`),
  CONSTRAINT `tank_certificate_ibfk_1` FOREIGN KEY (`tank_id`) REFERENCES `tank_header` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_certificate`
--

LOCK TABLES `tank_certificate` WRITE;
/*!40000 ALTER TABLE `tank_certificate` DISABLE KEYS */;
INSERT INTO `tank_certificate` VALUES (1,1,'IGEU 8899860',NULL,'2025-11-16','2025-11-09','BV','123','certificates/IGEU 8899860/IGEU 8899860_certificates.jpg','User',NULL,'2025-11-26 10:20:22','2025-11-26 10:20:22'),(2,1,'IGEU 8899860',NULL,'2025-11-23','2025-11-30','LR','7','certificates/IGEU 8899860/IGEU 8899860_certificates.jpeg','User',NULL,'2025-11-29 04:05:45','2025-11-29 04:05:45');
/*!40000 ALTER TABLE `tank_certificate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank_details`
--

DROP TABLE IF EXISTS `tank_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tank_id` int DEFAULT NULL,
  `tank_number` varchar(50) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `mfgr` varchar(255) DEFAULT NULL,
  `date_mfg` date DEFAULT NULL,
  `pv_code` varchar(255) DEFAULT NULL,
  `un_iso_code` varchar(255) DEFAULT NULL,
  `capacity_l` float DEFAULT NULL,
  `mawp` float DEFAULT NULL,
  `design_temperature` varchar(50) DEFAULT NULL,
  `tare_weight_kg` float DEFAULT NULL,
  `mgw_kg` float DEFAULT NULL,
  `mpl_kg` float DEFAULT NULL,
  `size` varchar(100) DEFAULT NULL,
  `pump_type` varchar(100) DEFAULT NULL,
  `vesmat` varchar(255) DEFAULT NULL,
  `gross_kg` float DEFAULT NULL,
  `net_kg` float DEFAULT NULL,
  `color_body_frame` varchar(255) DEFAULT NULL,
  `working_pressure` float DEFAULT NULL,
  `cabinet_type` varchar(100) DEFAULT NULL,
  `frame_type` varchar(100) DEFAULT NULL,
  `remark` text,
  `lease` tinyint(1) DEFAULT NULL,
  `created_by` varchar(255) DEFAULT NULL,
  `updated_by` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tank_id` (`tank_id`),
  KEY `tank_number` (`tank_number`),
  KEY `ix_tank_details_id` (`id`),
  CONSTRAINT `tank_details_ibfk_1` FOREIGN KEY (`tank_id`) REFERENCES `tank_header` (`id`),
  CONSTRAINT `tank_details_ibfk_2` FOREIGN KEY (`tank_number`) REFERENCES `tank_header` (`tank_number`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_details`
--

LOCK TABLES `tank_details` WRITE;
/*!40000 ALTER TABLE `tank_details` DISABLE KEYS */;
INSERT INTO `tank_details` VALUES (1,1,'IGEU 8899860','active','Unviersal','2025-11-19','GB150 / IMDF','T11',25000,11,'-196°C to 50°C',12000,10000,12346,'20\'','Yes','Carbon Steel SA-516 Gr. 70',4850,4200,'Safety Yellow',100,'yes','normal','Outlet valve requires inspection during next service. Fitted with pressure relief device P RD-456',0,'Admin',NULL),(2,3,'IGEU 8899861','active','Global','2025-11-18','GB150 / IMDF','T11',25000,11,'-196°C to 50°C',12000,11111,12346,'21\'','Yes','Carbon Steel SA-516 Gr. 71',4851,4200,'Safety Yellow',100,'yes','normal','Outlet valve requires inspection during next service. Fitted with pressure relief device P RD-456',1,'Admin',NULL),(3,4,'IGEU 8899862','active','Unviersal','2025-11-03','GB150 / IMDF','T11',25000,12,'-196°C to 50°C',12000,10000,12346,'21\'','Yes','Carbon Steel SA-516 Gr. 71',4851,4200,'Orange',NULL,'yes','normal','Outlet valve requires inspection during next service. Fitted with pressure relief device P RD-456',1,'Admin',NULL);
/*!40000 ALTER TABLE `tank_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank_drawings`
--

DROP TABLE IF EXISTS `tank_drawings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_drawings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tank_id` int NOT NULL,
  `drawing_type` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `original_filename` varchar(255) NOT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `tank_id` (`tank_id`),
  KEY `ix_tank_drawings_id` (`id`),
  CONSTRAINT `tank_drawings_ibfk_1` FOREIGN KEY (`tank_id`) REFERENCES `tank_header` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_drawings`
--

LOCK TABLES `tank_drawings` WRITE;
/*!40000 ALTER TABLE `tank_drawings` DISABLE KEYS */;
INSERT INTO `tank_drawings` VALUES (1,1,'PFD (Process Flow Diagram)','P and ID','drawings/IGEU 8899860/IGEU 8899860_drawings.jpg','boy-studying-with-book_113065-238-626x445.jpg','Admin','2025-11-26 10:22:07'),(2,1,'P&ID (Piping & Instrumentation Diagram)','P and ID','drawings/IGEU 8899860/IGEU 8899860_drawings.jpg','boy-studying-with-book_113065-238-626x445.jpg','Admin','2025-11-29 04:06:13');
/*!40000 ALTER TABLE `tank_drawings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank_header`
--

DROP TABLE IF EXISTS `tank_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_header` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tank_number` varchar(50) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  `created_by` varchar(100) DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tank_number` (`tank_number`),
  KEY `ix_tank_header_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_header`
--

LOCK TABLES `tank_header` WRITE;
/*!40000 ALTER TABLE `tank_header` DISABLE KEYS */;
INSERT INTO `tank_header` VALUES (1,'IGEU 8899860','active','2025-11-26 10:18:42','2025-11-29 04:25:43','Admin',NULL),(3,'IGEU 8899861','active','2025-11-29 03:59:33','2025-11-29 03:59:34','Admin',NULL),(4,'IGEU 8899862','active','2025-11-29 04:04:13','2025-11-29 04:04:13','Admin',NULL);
/*!40000 ALTER TABLE `tank_header` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank_images`
--

DROP TABLE IF EXISTS `tank_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `emp_id` int DEFAULT NULL,
  `tank_number` varchar(50) NOT NULL,
  `image_type` varchar(50) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `thumbnail_path` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `inspection_id` int DEFAULT NULL,
  `image_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_tank_image_daily` (`tank_number`,`image_type`,`created_date`),
  KEY `emp_id` (`emp_id`),
  KEY `idx_tank_image_type` (`tank_number`,`image_type`),
  KEY `idx_tank_number` (`tank_number`),
  KEY `idx_created_date` (`created_date`),
  KEY `ix_tank_images_id` (`id`),
  KEY `idx_inspection_id` (`inspection_id`),
  KEY `idx_image_id` (`image_id`),
  CONSTRAINT `fk_tank_images_image_type` FOREIGN KEY (`image_id`) REFERENCES `image_type` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_tank_images_inspection` FOREIGN KEY (`inspection_id`) REFERENCES `tank_inspection_details` (`inspection_id`) ON DELETE SET NULL,
  CONSTRAINT `tank_images_ibfk_1` FOREIGN KEY (`emp_id`) REFERENCES `users` (`emp_id`) ON DELETE SET NULL,
  CONSTRAINT `tank_images_ibfk_2` FOREIGN KEY (`tank_number`) REFERENCES `tank_header` (`tank_number`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_images`
--

LOCK TABLES `tank_images` WRITE;
/*!40000 ALTER TABLE `tank_images` DISABLE KEYS */;
INSERT INTO `tank_images` VALUES (1,NULL,'IGEU 8899860','front_view','IGEU 8899860/originals/IGEU 8899860_front_view_6e63872818ab4d3d866cc7876ca4d0bd.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_front_view_c2d6f584e944426595f0ee5ec61e5099_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,1),(2,NULL,'IGEU 8899860','rear_view','IGEU 8899860/originals/IGEU 8899860_rear_view_ae514a7babea4755bc88a3ff1e6c22ca.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_rear_view_8d5b8a1377ce46d68269098488e9c200_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,2),(3,NULL,'IGEU 8899860','top_view','IGEU 8899860/originals/IGEU 8899860_top_view_c37d174eb6db48e5900f44bc568ae95b.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_top_view_4219db51826e423d98da291964b056e3_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,3),(4,NULL,'IGEU 8899860','undersideview01','IGEU 8899860/originals/IGEU 8899860_undersideview01_a5fd19806175493eb0efc5ca7c9df4d0.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_undersideview01_67f9fa541701431fb6dedf7220dd14f2_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,4),(5,NULL,'IGEU 8899860','undersideview02','IGEU 8899860/originals/IGEU 8899860_undersideview02_869869e1a14945278cb94ab6a9c4385c.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_undersideview02_9eb85526cf4a425ab48295badef00d26_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,15),(6,NULL,'IGEU 8899860','front_lh_view','IGEU 8899860/originals/IGEU 8899860_front_lh_view_38fdeb19b2274f8c805f8b2694ff0cc3.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_front_lh_view_adc3e56308bc43b387112d4ddaf15706_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,5),(7,NULL,'IGEU 8899860','rear_lh_view','IGEU 8899860/originals/IGEU 8899860_rear_lh_view_23285877c414469d96565565bb50b35b.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_rear_lh_view_78960f8f2dde421eb44485ff8416919b_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,6),(8,NULL,'IGEU 8899860','front_rh_view','IGEU 8899860/originals/IGEU 8899860_front_rh_view_e70c768ec91547529aa67fbb263694cb.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_front_rh_view_ba1a66395fd54299b2dd4ad342b56715_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,7),(9,NULL,'IGEU 8899860','rear_rh_view','IGEU 8899860/originals/IGEU 8899860_rear_rh_view_8cf3ef8330ad4f1197fd938ff1652987.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_rear_rh_view_2be8e5466d6f4d98b0296c3886f7dfc3_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,8),(10,NULL,'IGEU 8899860','lh_side_view','IGEU 8899860/originals/IGEU 8899860_lh_side_view_24afdbfb3362438cb9d49d690b6dd9a4.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_lh_side_view_d452e8ffea314663b9821156f6ca446a_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,9),(11,NULL,'IGEU 8899860','rh_side_view','IGEU 8899860/originals/IGEU 8899860_rh_side_view_14f870e853ee447bac6a0d0e618ac927.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_rh_side_view_2a60ab2fcdc24559aecda228fee5dfa7_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,10),(12,NULL,'IGEU 8899860','valves_section_view','IGEU 8899860/originals/IGEU 8899860_valves_section_view_860f2cbefb3f4225a6aadbed000f3ce3.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_valves_section_view_aa0086619bbb48d7b08336d4381020c0_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,11),(13,NULL,'IGEU 8899860','safety_valve','IGEU 8899860/originals/IGEU 8899860_safety_valve_914567b3ace649618a3dfe43f3359e30.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_safety_valve_28f82c38b5cf425e9466ea5693c9bcc9_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,12),(14,NULL,'IGEU 8899860','level___pressure_gauge','IGEU 8899860/originals/IGEU 8899860_level___pressure_gauge_833d3264152f4562a3e700d28c99a2df.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_level___pressure_gauge_bd8c588b6a714bfd9fe7f2f5e4286301_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,13),(15,NULL,'IGEU 8899860','vacuum_reading','IGEU 8899860/originals/IGEU 8899860_vacuum_reading_cd6b54b2bbb441d1a96a73bcec5cd89f.jpeg','IGEU 8899860/thumbnails/IGEU 8899860_vacuum_reading_39abda1976ed4fb9a62169cf6824ec2e_thumb.jpg','2025-11-28 12:11:14','2025-11-28 12:11:14','2025-11-28 12:11:14',2,14);
/*!40000 ALTER TABLE `tank_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank_inspection`
--

DROP TABLE IF EXISTS `tank_inspection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_inspection` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tank_id` int NOT NULL,
  `insp_2_5y_date` date DEFAULT NULL,
  `next_insp_date` date DEFAULT NULL,
  `tank_certificate` varchar(255) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `tank_id` (`tank_id`),
  KEY `ix_tank_inspection_id` (`id`),
  CONSTRAINT `tank_inspection_ibfk_1` FOREIGN KEY (`tank_id`) REFERENCES `tank_header` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_inspection`
--

LOCK TABLES `tank_inspection` WRITE;
/*!40000 ALTER TABLE `tank_inspection` DISABLE KEYS */;
/*!40000 ALTER TABLE `tank_inspection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank_inspection_details`
--

DROP TABLE IF EXISTS `tank_inspection_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_inspection_details` (
  `inspection_id` int NOT NULL AUTO_INCREMENT,
  `inspection_date` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `report_number` varchar(50) NOT NULL,
  `tank_id` int DEFAULT NULL,
  `tank_number` varchar(50) NOT NULL,
  `status_id` int NOT NULL,
  `product_id` int NOT NULL,
  `inspection_type_id` int NOT NULL,
  `location_id` int NOT NULL,
  `working_pressure` decimal(12,2) DEFAULT NULL,
  `design_temperature` varchar(100) DEFAULT NULL,
  `frame_type` varchar(255) DEFAULT NULL,
  `cabinet_type` varchar(255) DEFAULT NULL,
  `mfgr` varchar(255) DEFAULT NULL,
  `safety_valve_brand_id` int DEFAULT NULL,
  `safety_valve_model_id` int DEFAULT NULL,
  `safety_valve_size_id` int DEFAULT NULL,
  `pi_next_inspection_date` date DEFAULT NULL,
  `notes` text,
  `lifter_weight` varchar(255) DEFAULT NULL,
  `emp_id` int DEFAULT NULL,
  `operator_id` int DEFAULT NULL,
  `ownership` varchar(16) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL,
  `lifter_weight_thumbnail` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`inspection_id`),
  UNIQUE KEY `ix_tank_inspection_details_report_number` (`report_number`),
  KEY `ix_tank_inspection_details_product_id` (`product_id`),
  KEY `ix_tank_inspection_details_tank_id` (`tank_id`),
  KEY `ix_tank_inspection_details_safety_valve_model_id` (`safety_valve_model_id`),
  KEY `ix_tank_inspection_details_operator_id` (`operator_id`),
  KEY `ix_tank_inspection_details_ownership` (`ownership`),
  KEY `ix_tank_inspection_details_tank_number` (`tank_number`),
  KEY `ix_tank_inspection_details_safety_valve_brand_id` (`safety_valve_brand_id`),
  KEY `ix_tank_inspection_details_emp_id` (`emp_id`),
  KEY `ix_tank_inspection_details_status_id` (`status_id`),
  KEY `ix_tank_inspection_details_inspection_id` (`inspection_id`),
  KEY `ix_tank_inspection_details_safety_valve_size_id` (`safety_valve_size_id`),
  CONSTRAINT `tank_inspection_details_ibfk_1` FOREIGN KEY (`tank_id`) REFERENCES `tank_details` (`tank_id`) ON DELETE SET NULL,
  CONSTRAINT `tank_inspection_details_ibfk_2` FOREIGN KEY (`emp_id`) REFERENCES `users` (`emp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_inspection_details`
--

LOCK TABLES `tank_inspection_details` WRITE;
/*!40000 ALTER TABLE `tank_inspection_details` DISABLE KEYS */;
INSERT INTO `tank_inspection_details` VALUES (2,'2025-11-29 13:11:56','2025-11-26 16:33:19','2025-11-29 20:58:57','RPT-1764154999',1,'IGEU 8899860',2,1,1,1,11.00,'50.00','Unviersal',NULL,NULL,1,1,1,'2025-11-19','Outlet valve requires inspection during next service. Fitted with pressure relief device P RD-4560','IGEU 8899860/IGEU 8899860_lifter_weight_ad41f046f5c74237aa8e162e278966e0.jpeg',1001,NULL,'Leased','Admin','Admin','IGEU 8899860/IGEU 8899860_lifter_weight_13e576ae9abe43f4aae24f40cf6051c8_thumb.jpg'),(4,'2025-11-29 13:11:56','2025-11-29 18:54:20','2025-11-29 21:11:58','SG-T1-29112025-01',1,'IGEU 8899860',2,1,1,1,100.00,'-196°C to 50°C','normal','yes','Unviersal',NULL,NULL,NULL,'2025-11-30','All checks ok',NULL,NULL,1001,'owned','naveen@gmail.com','naveen@gmail.com',NULL),(5,'2025-11-29 21:18:46','2025-11-29 21:18:45','2025-11-29 21:18:45','SG-T1-29112025-03',1,'IGEU 8899860',1,2,2,3,100.00,'-196°C to 50°C','normal','yes','Unviersal',2,1,1,'2025-11-30','All checks ok',NULL,NULL,1001,'owned','naveen@gmail.com','naveen@gmail.com',NULL),(6,'2025-11-29 21:19:16','2025-11-29 21:19:15','2025-11-29 21:19:15','SG-T1-29112025-04',1,'IGEU 8899860',1,2,3,3,100.00,'-196°C to 50°C','normal','yes','Unviersal',NULL,NULL,NULL,'2025-11-30','All checks ok',NULL,NULL,1001,'owned','naveen@gmail.com','naveen@gmail.com',NULL);
/*!40000 ALTER TABLE `tank_inspection_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank_regulations`
--

DROP TABLE IF EXISTS `tank_regulations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_regulations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tank_id` int DEFAULT NULL,
  `regulation_id` int DEFAULT NULL,
  `initial_approval_no` varchar(100) DEFAULT NULL,
  `imo_type` varchar(100) DEFAULT NULL,
  `safety_standard` varchar(255) DEFAULT NULL,
  `regulation_name` varchar(255) DEFAULT NULL,
  `country_registration` varchar(100) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `tank_id` (`tank_id`),
  KEY `regulation_id` (`regulation_id`),
  KEY `ix_tank_regulations_id` (`id`),
  CONSTRAINT `tank_regulations_ibfk_1` FOREIGN KEY (`tank_id`) REFERENCES `tank_header` (`id`) ON DELETE CASCADE,
  CONSTRAINT `tank_regulations_ibfk_2` FOREIGN KEY (`regulation_id`) REFERENCES `regulations_master` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_regulations`
--

LOCK TABLES `tank_regulations` WRITE;
/*!40000 ALTER TABLE `tank_regulations` DISABLE KEYS */;
INSERT INTO `tank_regulations` VALUES (1,1,1,'AP-2025-005','IMO-T11','EN 1445',NULL,'IND','Admin',NULL,'2025-11-28 15:08:57','2025-11-28 15:08:57'),(2,1,1,'AP-2025-005','IMO-T11','EN 1444',NULL,'IND','Admin',NULL,'2025-11-29 04:04:37','2025-11-29 04:04:37');
/*!40000 ALTER TABLE `tank_regulations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tank_status`
--

DROP TABLE IF EXISTS `tank_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tank_status` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `status_name` varchar(150) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`status_id`),
  UNIQUE KEY `status_name` (`status_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tank_status`
--

LOCK TABLES `tank_status` WRITE;
/*!40000 ALTER TABLE `tank_status` DISABLE KEYS */;
INSERT INTO `tank_status` VALUES (1,'Laden','Tank is loaded / filled',NULL,NULL),(2,'Empty','Tank is empty',NULL,NULL),(3,'Residue','Only residue remains',NULL,NULL);
/*!40000 ALTER TABLE `tank_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `to_do_list`
--

DROP TABLE IF EXISTS `to_do_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `to_do_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `checklist_id` int NOT NULL,
  `inspection_id` int NOT NULL,
  `tank_id` int DEFAULT NULL,
  `job_name` varchar(255) DEFAULT NULL,
  `sub_job_description` varchar(512) DEFAULT NULL,
  `sn` varchar(16) NOT NULL,
  `status_id` int DEFAULT NULL,
  `comment` text,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_to_do_list_checklist_id` (`checklist_id`),
  KEY `ix_to_do_list_tank_id` (`tank_id`),
  KEY `ix_to_do_list_inspection_id` (`inspection_id`),
  KEY `ix_to_do_list_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `to_do_list`
--

LOCK TABLES `to_do_list` WRITE;
/*!40000 ALTER TABLE `to_do_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `to_do_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `emp_id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `designation` varchar(255) DEFAULT NULL,
  `hod` varchar(255) DEFAULT NULL,
  `supervisor` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `password_salt` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  `role` varchar(50) NOT NULL DEFAULT 'user',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `ix_users_emp_id` (`emp_id`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,1001,'naveen','string','string','string','string','naveen@gmail.com','9ae28de23c16d8c586094d75c48b43cde24fbd46dc47d9acaac2872ec1a9dcd5','a1d6f6f876148c560f6c3ed734c1a2c3','2025-11-27 14:14:37','2025-11-27 14:14:37','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valve_test_report`
--

DROP TABLE IF EXISTS `valve_test_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valve_test_report` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tank_id` int NOT NULL,
  `inspection_report_file` varchar(255) DEFAULT NULL,
  `test_date` date DEFAULT NULL,
  `inspected_by` varchar(100) DEFAULT NULL,
  `remarks` text,
  `created_by` varchar(100) DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT (now()),
  `updated_at` timestamp NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `tank_id` (`tank_id`),
  KEY `ix_valve_test_report_id` (`id`),
  CONSTRAINT `valve_test_report_ibfk_1` FOREIGN KEY (`tank_id`) REFERENCES `tank_header` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valve_test_report`
--

LOCK TABLES `valve_test_report` WRITE;
/*!40000 ALTER TABLE `valve_test_report` DISABLE KEYS */;
INSERT INTO `valve_test_report` VALUES (2,1,'valve_reports/IGEU 8899860/IGEU 8899860_valve_reports.jpg','2025-11-30','admin','no issues.','User',NULL,'2025-11-29 04:07:18','2025-11-29 04:07:18');
/*!40000 ALTER TABLE `valve_test_report` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-01 18:47:33
