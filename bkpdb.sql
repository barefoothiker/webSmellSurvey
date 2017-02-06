-- MySQL dump 10.13  Distrib 5.6.22, for osx10.8 (x86_64)
--
-- Host: localhost    Database: smellsurveydb
-- ------------------------------------------------------
-- Server version	5.6.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add ontology type',7,'add_ontologytype'),(20,'Can change ontology type',7,'change_ontologytype'),(21,'Can delete ontology type',7,'delete_ontologytype'),(22,'Can add ontology',8,'add_ontology'),(23,'Can change ontology',8,'change_ontology'),(24,'Can delete ontology',8,'delete_ontology'),(25,'Can add question answer type',9,'add_questionanswertype'),(26,'Can change question answer type',9,'change_questionanswertype'),(27,'Can delete question answer type',9,'delete_questionanswertype'),(28,'Can add question answer data type',10,'add_questionanswerdatatype'),(29,'Can change question answer data type',10,'change_questionanswerdatatype'),(30,'Can delete question answer data type',10,'delete_questionanswerdatatype'),(31,'Can add language',11,'add_language'),(32,'Can change language',11,'change_language'),(33,'Can delete language',11,'delete_language'),(34,'Can add questionnaire',12,'add_questionnaire'),(35,'Can change questionnaire',12,'change_questionnaire'),(36,'Can delete questionnaire',12,'delete_questionnaire'),(37,'Can add section',13,'add_section'),(38,'Can change section',13,'change_section'),(39,'Can delete section',13,'delete_section'),(40,'Can add question answer',14,'add_questionanswer'),(41,'Can change question answer',14,'change_questionanswer'),(42,'Can delete question answer',14,'delete_questionanswer'),(43,'Can add question answer choice',15,'add_questionanswerchoice'),(44,'Can change question answer choice',15,'change_questionanswerchoice'),(45,'Can delete question answer choice',15,'delete_questionanswerchoice'),(46,'Can add question',16,'add_question'),(47,'Can change question',16,'change_question'),(48,'Can delete question',16,'delete_question'),(49,'Can add role',17,'add_role'),(50,'Can change role',17,'change_role'),(51,'Can delete role',17,'delete_role'),(52,'Can add site',18,'add_site'),(53,'Can change site',18,'change_site'),(54,'Can delete site',18,'delete_site'),(55,'Can add study',19,'add_study'),(56,'Can change study',19,'change_study'),(57,'Can delete study',19,'delete_study'),(58,'Can add survey user',20,'add_surveyuser'),(59,'Can change survey user',20,'change_surveyuser'),(60,'Can delete survey user',20,'delete_surveyuser'),(61,'Can add administrator',21,'add_administrator'),(62,'Can change administrator',21,'change_administrator'),(63,'Can delete administrator',21,'delete_administrator'),(64,'Can add patient',22,'add_patient'),(65,'Can change patient',22,'change_patient'),(66,'Can delete patient',22,'delete_patient'),(67,'Can add upin',23,'add_upin'),(68,'Can change upin',23,'change_upin'),(69,'Can delete upin',23,'delete_upin'),(70,'Can add administration',24,'add_administration'),(71,'Can change administration',24,'change_administration'),(72,'Can delete administration',24,'delete_administration'),(73,'Can add question answer instance',25,'add_questionanswerinstance'),(74,'Can change question answer instance',25,'change_questionanswerinstance'),(75,'Can delete question answer instance',25,'delete_questionanswerinstance'),(76,'Can add registration profile',26,'add_registrationprofile'),(77,'Can change registration profile',26,'change_registrationprofile'),(78,'Can delete registration profile',26,'delete_registrationprofile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$24000$V8x8AHcE7ziP$YOwZuyWevILO3LASURVaAQ3VYQ39fL25/HWfXmgSe9s=',NULL,1,'a','','','a@a.com',1,1,'2016-11-04 14:20:05.425578');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(26,'registration','registrationprofile'),(6,'sessions','session'),(24,'smellSurvey','administration'),(21,'smellSurvey','administrator'),(11,'smellSurvey','language'),(8,'smellSurvey','ontology'),(7,'smellSurvey','ontologytype'),(22,'smellSurvey','patient'),(16,'smellSurvey','question'),(14,'smellSurvey','questionanswer'),(15,'smellSurvey','questionanswerchoice'),(10,'smellSurvey','questionanswerdatatype'),(25,'smellSurvey','questionanswerinstance'),(9,'smellSurvey','questionanswertype'),(12,'smellSurvey','questionnaire'),(17,'smellSurvey','role'),(13,'smellSurvey','section'),(18,'smellSurvey','site'),(19,'smellSurvey','study'),(20,'smellSurvey','surveyuser'),(23,'smellSurvey','upin');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-11-04 14:19:24.396345'),(2,'auth','0001_initial','2016-11-04 14:19:28.542349'),(3,'admin','0001_initial','2016-11-04 14:19:29.304773'),(4,'admin','0002_logentry_remove_auto_add','2016-11-04 14:19:29.623128'),(5,'contenttypes','0002_remove_content_type_name','2016-11-04 14:19:29.990908'),(6,'auth','0002_alter_permission_name_max_length','2016-11-04 14:19:30.180074'),(7,'auth','0003_alter_user_email_max_length','2016-11-04 14:19:30.357237'),(8,'auth','0004_alter_user_username_opts','2016-11-04 14:19:30.366865'),(9,'auth','0005_alter_user_last_login_null','2016-11-04 14:19:30.503256'),(10,'auth','0006_require_contenttypes_0002','2016-11-04 14:19:30.505314'),(11,'auth','0007_alter_validators_add_error_messages','2016-11-04 14:19:30.514983'),(12,'registration','0001_initial','2016-11-04 14:19:30.815131'),(13,'sessions','0001_initial','2016-11-04 14:19:31.068850'),(14,'smellSurvey','0001_initial','2016-11-04 14:19:49.852922');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration_registrationprofile`
--

DROP TABLE IF EXISTS `registration_registrationprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registration_registrationprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activation_key` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `registration_registrationprofil_user_id_5fcbf725_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration_registrationprofile`
--

LOCK TABLES `registration_registrationprofile` WRITE;
/*!40000 ALTER TABLE `registration_registrationprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `registration_registrationprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_administration`
--

DROP TABLE IF EXISTS `smellSurvey_administration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_administration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `startTime` datetime(6) DEFAULT NULL,
  `stopTime` datetime(6) DEFAULT NULL,
  `questionnaire_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  `upin_id` int(11) NOT NULL,
  `administrator_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `smellSurvey_administration_a5301291` (`questionnaire_id`),
  KEY `smellSurvey_administration_9365d6e7` (`site_id`),
  KEY `smellSurvey_administration_70d7596e` (`upin_id`),
  KEY `smellSurvey_administration_a68d6894` (`administrator_id`),
  CONSTRAINT `e9b0b04b20ad11686656e1ab35864847` FOREIGN KEY (`administrator_id`) REFERENCES `smellSurvey_administrator` (`surveyuser_ptr_id`),
  CONSTRAINT `smellS_questionnaire_id_578b2f9d_fk_smellSurvey_questionnaire_id` FOREIGN KEY (`questionnaire_id`) REFERENCES `smellSurvey_questionnaire` (`id`),
  CONSTRAINT `smellSurvey_administrati_site_id_0c493c50_fk_smellSurvey_site_id` FOREIGN KEY (`site_id`) REFERENCES `smellSurvey_site` (`id`),
  CONSTRAINT `smellSurvey_administrati_upin_id_d75da59a_fk_smellSurvey_upin_id` FOREIGN KEY (`upin_id`) REFERENCES `smellSurvey_upin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_administration`
--

LOCK TABLES `smellSurvey_administration` WRITE;
/*!40000 ALTER TABLE `smellSurvey_administration` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_administration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_administrator`
--

DROP TABLE IF EXISTS `smellSurvey_administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_administrator` (
  `surveyuser_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`surveyuser_ptr_id`),
  CONSTRAINT `smellSur_surveyuser_ptr_id_abbcc976_fk_smellSurvey_surveyuser_id` FOREIGN KEY (`surveyuser_ptr_id`) REFERENCES `smellSurvey_surveyuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_administrator`
--

LOCK TABLES `smellSurvey_administrator` WRITE;
/*!40000 ALTER TABLE `smellSurvey_administrator` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_administrator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_administrator_allowedSites`
--

DROP TABLE IF EXISTS `smellSurvey_administrator_allowedSites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_administrator_allowedSites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `administrator_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `smellSurvey_administrator_allowed_administrator_id_19f15673_uniq` (`administrator_id`,`site_id`),
  KEY `smellSurvey_administrato_site_id_2a67a56d_fk_smellSurvey_site_id` (`site_id`),
  CONSTRAINT `D531d11293a6ef7fd427ad63c318d1b7` FOREIGN KEY (`administrator_id`) REFERENCES `smellSurvey_administrator` (`surveyuser_ptr_id`),
  CONSTRAINT `smellSurvey_administrato_site_id_2a67a56d_fk_smellSurvey_site_id` FOREIGN KEY (`site_id`) REFERENCES `smellSurvey_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_administrator_allowedSites`
--

LOCK TABLES `smellSurvey_administrator_allowedSites` WRITE;
/*!40000 ALTER TABLE `smellSurvey_administrator_allowedSites` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_administrator_allowedSites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_administrator_allowedStudies`
--

DROP TABLE IF EXISTS `smellSurvey_administrator_allowedStudies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_administrator_allowedStudies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `administrator_id` int(11) NOT NULL,
  `study_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `smellSurvey_administrator_allowed_administrator_id_c88e9b8d_uniq` (`administrator_id`,`study_id`),
  KEY `smellSurvey_administra_study_id_921268f2_fk_smellSurvey_study_id` (`study_id`),
  CONSTRAINT `b4647afec00237b76eee485d546d1401` FOREIGN KEY (`administrator_id`) REFERENCES `smellSurvey_administrator` (`surveyuser_ptr_id`),
  CONSTRAINT `smellSurvey_administra_study_id_921268f2_fk_smellSurvey_study_id` FOREIGN KEY (`study_id`) REFERENCES `smellSurvey_study` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_administrator_allowedStudies`
--

LOCK TABLES `smellSurvey_administrator_allowedStudies` WRITE;
/*!40000 ALTER TABLE `smellSurvey_administrator_allowedStudies` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_administrator_allowedStudies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_language`
--

DROP TABLE IF EXISTS `smellSurvey_language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_language`
--

LOCK TABLES `smellSurvey_language` WRITE;
/*!40000 ALTER TABLE `smellSurvey_language` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_language` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_ontology`
--

DROP TABLE IF EXISTS `smellSurvey_ontology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_ontology` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `ontologyType_id` int(11),
  `parent_id` int(11),
  PRIMARY KEY (`id`),
  KEY `smellSurvey_ontology_d246fb4f` (`ontologyType_id`),
  KEY `smellSurvey_ontology_6be37982` (`parent_id`),
  CONSTRAINT `smellSur_ontologyType_id_7dffa5c9_fk_smellSurvey_ontologytype_id` FOREIGN KEY (`ontologyType_id`) REFERENCES `smellSurvey_ontologytype` (`id`),
  CONSTRAINT `smellSurvey_ontolo_parent_id_ca523524_fk_smellSurvey_ontology_id` FOREIGN KEY (`parent_id`) REFERENCES `smellSurvey_ontology` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_ontology`
--

LOCK TABLES `smellSurvey_ontology` WRITE;
/*!40000 ALTER TABLE `smellSurvey_ontology` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_ontology` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_ontologytype`
--

DROP TABLE IF EXISTS `smellSurvey_ontologytype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_ontologytype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_ontologytype`
--

LOCK TABLES `smellSurvey_ontologytype` WRITE;
/*!40000 ALTER TABLE `smellSurvey_ontologytype` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_ontologytype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_patient`
--

DROP TABLE IF EXISTS `smellSurvey_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_patient` (
  `surveyuser_ptr_id` int(11) NOT NULL,
  `defaultAdministrator_id` int(11) NOT NULL,
  `defaultSite_id` int(11) NOT NULL,
  `defaultStudy_id` int(11) NOT NULL,
  PRIMARY KEY (`surveyuser_ptr_id`),
  KEY `c8333fefe21d7fd5cf404fd458c26788` (`defaultAdministrator_id`),
  KEY `smellSurvey_patie_defaultSite_id_6d7c5222_fk_smellSurvey_site_id` (`defaultSite_id`),
  KEY `smellSurvey_pat_defaultStudy_id_4bc03a20_fk_smellSurvey_study_id` (`defaultStudy_id`),
  CONSTRAINT `c8333fefe21d7fd5cf404fd458c26788` FOREIGN KEY (`defaultAdministrator_id`) REFERENCES `smellSurvey_administrator` (`surveyuser_ptr_id`),
  CONSTRAINT `smellSur_surveyuser_ptr_id_151b4b85_fk_smellSurvey_surveyuser_id` FOREIGN KEY (`surveyuser_ptr_id`) REFERENCES `smellSurvey_surveyuser` (`id`),
  CONSTRAINT `smellSurvey_pat_defaultStudy_id_4bc03a20_fk_smellSurvey_study_id` FOREIGN KEY (`defaultStudy_id`) REFERENCES `smellSurvey_study` (`id`),
  CONSTRAINT `smellSurvey_patie_defaultSite_id_6d7c5222_fk_smellSurvey_site_id` FOREIGN KEY (`defaultSite_id`) REFERENCES `smellSurvey_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_patient`
--

LOCK TABLES `smellSurvey_patient` WRITE;
/*!40000 ALTER TABLE `smellSurvey_patient` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_patient_studies`
--

DROP TABLE IF EXISTS `smellSurvey_patient_studies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_patient_studies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `study_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `smellSurvey_patient_studies_patient_id_ae9973d0_uniq` (`patient_id`,`study_id`),
  KEY `smellSurvey_patient_st_study_id_7c9d5ae9_fk_smellSurvey_study_id` (`study_id`),
  CONSTRAINT `sme_patient_id_229e0d4e_fk_smellSurvey_patient_surveyuser_ptr_id` FOREIGN KEY (`patient_id`) REFERENCES `smellSurvey_patient` (`surveyuser_ptr_id`),
  CONSTRAINT `smellSurvey_patient_st_study_id_7c9d5ae9_fk_smellSurvey_study_id` FOREIGN KEY (`study_id`) REFERENCES `smellSurvey_study` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_patient_studies`
--

LOCK TABLES `smellSurvey_patient_studies` WRITE;
/*!40000 ALTER TABLE `smellSurvey_patient_studies` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_patient_studies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_question`
--

DROP TABLE IF EXISTS `smellSurvey_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `questionId` int(11) NOT NULL,
  `ontologyClassSubClass_id` int(11),
  `ontologyIndividual_id` int(11),
  `parent_id` int(11),
  `parentAnswer_id` int(11),
  `section_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `smellSurvey_question_cb773a60` (`ontologyClassSubClass_id`),
  KEY `smellSurvey_question_bf1f2780` (`ontologyIndividual_id`),
  KEY `smellSurvey_question_6be37982` (`parent_id`),
  KEY `smellSurvey_question_95f09c99` (`parentAnswer_id`),
  KEY `smellSurvey_question_730f6511` (`section_id`),
  CONSTRAINT `sme_ontologyClassSubClass_id_3d75e9ec_fk_smellSurvey_ontology_id` FOREIGN KEY (`ontologyClassSubClass_id`) REFERENCES `smellSurvey_ontology` (`id`),
  CONSTRAINT `smellS_ontologyIndividual_id_0a31f65e_fk_smellSurvey_ontology_id` FOREIGN KEY (`ontologyIndividual_id`) REFERENCES `smellSurvey_ontology` (`id`),
  CONSTRAINT `smellS_parentAnswer_id_13675e17_fk_smellSurvey_questionanswer_id` FOREIGN KEY (`parentAnswer_id`) REFERENCES `smellSurvey_questionanswer` (`id`),
  CONSTRAINT `smellSurvey_questi_parent_id_cf255cce_fk_smellSurvey_question_id` FOREIGN KEY (`parent_id`) REFERENCES `smellSurvey_question` (`id`),
  CONSTRAINT `smellSurvey_questi_section_id_8e43491b_fk_smellSurvey_section_id` FOREIGN KEY (`section_id`) REFERENCES `smellSurvey_section` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_question`
--

LOCK TABLES `smellSurvey_question` WRITE;
/*!40000 ALTER TABLE `smellSurvey_question` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_question_answers`
--

DROP TABLE IF EXISTS `smellSurvey_question_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_question_answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `questionanswer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `smellSurvey_question_answers_question_id_2e7d841f_uniq` (`question_id`,`questionanswer_id`),
  KEY `smel_questionanswer_id_b41180b6_fk_smellSurvey_questionanswer_id` (`questionanswer_id`),
  CONSTRAINT `smel_questionanswer_id_b41180b6_fk_smellSurvey_questionanswer_id` FOREIGN KEY (`questionanswer_id`) REFERENCES `smellSurvey_questionanswer` (`id`),
  CONSTRAINT `smellSurvey_ques_question_id_12b76706_fk_smellSurvey_question_id` FOREIGN KEY (`question_id`) REFERENCES `smellSurvey_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_question_answers`
--

LOCK TABLES `smellSurvey_question_answers` WRITE;
/*!40000 ALTER TABLE `smellSurvey_question_answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_question_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_questionanswer`
--

DROP TABLE IF EXISTS `smellSurvey_questionanswer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_questionanswer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(256) NOT NULL,
  `questionAnswerId` int(11) NOT NULL,
  `questionAnswerRangeLower` int(11) DEFAULT NULL,
  `questionAnswerRangeUpper` int(11) DEFAULT NULL,
  `requiredFlag` tinyint(1) DEFAULT NULL,
  `phiFlag` tinyint(1) DEFAULT NULL,
  `pictureURL` varchar(256) DEFAULT NULL,
  `questionAnswerOntology_id` int(11) DEFAULT NULL,
  `questionAnswerType_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sm_questionAnswerOntology_id_2a76c333_fk_smellSurvey_ontology_id` (`questionAnswerOntology_id`),
  KEY `smellSurvey_questionanswer_648e61f6` (`questionAnswerType_id`),
  CONSTRAINT `f0e9ece4a4529afd1faed56e1ad511af` FOREIGN KEY (`questionAnswerType_id`) REFERENCES `smellSurvey_questionanswertype` (`id`),
  CONSTRAINT `sm_questionAnswerOntology_id_2a76c333_fk_smellSurvey_ontology_id` FOREIGN KEY (`questionAnswerOntology_id`) REFERENCES `smellSurvey_ontology` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_questionanswer`
--

LOCK TABLES `smellSurvey_questionanswer` WRITE;
/*!40000 ALTER TABLE `smellSurvey_questionanswer` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_questionanswer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_questionanswerchoice`
--

DROP TABLE IF EXISTS `smellSurvey_questionanswerchoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_questionanswerchoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(256) NOT NULL,
  `choiceOntology_id` int(11) DEFAULT NULL,
  `questionAnswer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `smellSurve_choiceOntology_id_79b9f850_fk_smellSurvey_ontology_id` (`choiceOntology_id`),
  KEY `smel_questionAnswer_id_d753b40c_fk_smellSurvey_questionanswer_id` (`questionAnswer_id`),
  CONSTRAINT `smel_questionAnswer_id_d753b40c_fk_smellSurvey_questionanswer_id` FOREIGN KEY (`questionAnswer_id`) REFERENCES `smellSurvey_questionanswer` (`id`),
  CONSTRAINT `smellSurve_choiceOntology_id_79b9f850_fk_smellSurvey_ontology_id` FOREIGN KEY (`choiceOntology_id`) REFERENCES `smellSurvey_ontology` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_questionanswerchoice`
--

LOCK TABLES `smellSurvey_questionanswerchoice` WRITE;
/*!40000 ALTER TABLE `smellSurvey_questionanswerchoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_questionanswerchoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_questionanswerdatatype`
--

DROP TABLE IF EXISTS `smellSurvey_questionanswerdatatype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_questionanswerdatatype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_questionanswerdatatype`
--

LOCK TABLES `smellSurvey_questionanswerdatatype` WRITE;
/*!40000 ALTER TABLE `smellSurvey_questionanswerdatatype` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_questionanswerdatatype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_questionanswerinstance`
--

DROP TABLE IF EXISTS `smellSurvey_questionanswerinstance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_questionanswerinstance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timeStamp` datetime(6) DEFAULT NULL,
  `answerText` varchar(256) DEFAULT NULL,
  `administration_id` int(11) NOT NULL,
  `answer_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `smel_administration_id_09edad1f_fk_smellSurvey_administration_id` (`administration_id`),
  KEY `smellSurvey__answer_id_7bbfed03_fk_smellSurvey_questionanswer_id` (`answer_id`),
  KEY `smellSurvey_ques_question_id_10a77c96_fk_smellSurvey_question_id` (`question_id`),
  CONSTRAINT `smel_administration_id_09edad1f_fk_smellSurvey_administration_id` FOREIGN KEY (`administration_id`) REFERENCES `smellSurvey_administration` (`id`),
  CONSTRAINT `smellSurvey__answer_id_7bbfed03_fk_smellSurvey_questionanswer_id` FOREIGN KEY (`answer_id`) REFERENCES `smellSurvey_questionanswer` (`id`),
  CONSTRAINT `smellSurvey_ques_question_id_10a77c96_fk_smellSurvey_question_id` FOREIGN KEY (`question_id`) REFERENCES `smellSurvey_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_questionanswerinstance`
--

LOCK TABLES `smellSurvey_questionanswerinstance` WRITE;
/*!40000 ALTER TABLE `smellSurvey_questionanswerinstance` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_questionanswerinstance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_questionanswertype`
--

DROP TABLE IF EXISTS `smellSurvey_questionanswertype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_questionanswertype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_questionanswertype`
--

LOCK TABLES `smellSurvey_questionanswertype` WRITE;
/*!40000 ALTER TABLE `smellSurvey_questionanswertype` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_questionanswertype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_questionnaire`
--

DROP TABLE IF EXISTS `smellSurvey_questionnaire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_questionnaire` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `version` int(11) NOT NULL,
  `language_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `smellSurvey_ques_language_id_ee58336c_fk_smellSurvey_language_id` (`language_id`),
  CONSTRAINT `smellSurvey_ques_language_id_ee58336c_fk_smellSurvey_language_id` FOREIGN KEY (`language_id`) REFERENCES `smellSurvey_language` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_questionnaire`
--

LOCK TABLES `smellSurvey_questionnaire` WRITE;
/*!40000 ALTER TABLE `smellSurvey_questionnaire` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_questionnaire` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_role`
--

DROP TABLE IF EXISTS `smellSurvey_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `isSuperUser` tinyint(1) NOT NULL,
  `isAdministrator` tinyint(1) NOT NULL,
  `isPatient` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_role`
--

LOCK TABLES `smellSurvey_role` WRITE;
/*!40000 ALTER TABLE `smellSurvey_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_section`
--

DROP TABLE IF EXISTS `smellSurvey_section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_section` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `sequence` int(11) NOT NULL,
  `questionnaire_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `smellS_questionnaire_id_66faef69_fk_smellSurvey_questionnaire_id` (`questionnaire_id`),
  CONSTRAINT `smellS_questionnaire_id_66faef69_fk_smellSurvey_questionnaire_id` FOREIGN KEY (`questionnaire_id`) REFERENCES `smellSurvey_questionnaire` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_section`
--

LOCK TABLES `smellSurvey_section` WRITE;
/*!40000 ALTER TABLE `smellSurvey_section` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_site`
--

DROP TABLE IF EXISTS `smellSurvey_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(512) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_site`
--

LOCK TABLES `smellSurvey_site` WRITE;
/*!40000 ALTER TABLE `smellSurvey_site` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_study`
--

DROP TABLE IF EXISTS `smellSurvey_study`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_study` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(512) NOT NULL,
  `questionnaire_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `smellS_questionnaire_id_3fd8dfaf_fk_smellSurvey_questionnaire_id` (`questionnaire_id`),
  CONSTRAINT `smellS_questionnaire_id_3fd8dfaf_fk_smellSurvey_questionnaire_id` FOREIGN KEY (`questionnaire_id`) REFERENCES `smellSurvey_questionnaire` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_study`
--

LOCK TABLES `smellSurvey_study` WRITE;
/*!40000 ALTER TABLE `smellSurvey_study` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_study` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_surveyuser`
--

DROP TABLE IF EXISTS `smellSurvey_surveyuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_surveyuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11),
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `smellSurvey_surveyuser_84566833` (`role_id`),
  KEY `smellSurvey_surveyuser_e8701ad4` (`user_id`),
  CONSTRAINT `smellSurvey_surveyuser_role_id_162cd803_fk_smellSurvey_role_id` FOREIGN KEY (`role_id`) REFERENCES `smellSurvey_role` (`id`),
  CONSTRAINT `smellSurvey_surveyuser_user_id_12b1a11c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_surveyuser`
--

LOCK TABLES `smellSurvey_surveyuser` WRITE;
/*!40000 ALTER TABLE `smellSurvey_surveyuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_surveyuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smellSurvey_upin`
--

DROP TABLE IF EXISTS `smellSurvey_upin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smellSurvey_upin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `upinId` int(11) NOT NULL,
  `study_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `smellSurvey_upin_study_id_265449fe_fk_smellSurvey_study_id` (`study_id`),
  KEY `smellSurvey_upin_9f065c57` (`patient_id`),
  CONSTRAINT `sme_patient_id_96a08da2_fk_smellSurvey_patient_surveyuser_ptr_id` FOREIGN KEY (`patient_id`) REFERENCES `smellSurvey_patient` (`surveyuser_ptr_id`),
  CONSTRAINT `smellSurvey_upin_study_id_265449fe_fk_smellSurvey_study_id` FOREIGN KEY (`study_id`) REFERENCES `smellSurvey_study` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smellSurvey_upin`
--

LOCK TABLES `smellSurvey_upin` WRITE;
/*!40000 ALTER TABLE `smellSurvey_upin` DISABLE KEYS */;
/*!40000 ALTER TABLE `smellSurvey_upin` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-04 10:20:29
