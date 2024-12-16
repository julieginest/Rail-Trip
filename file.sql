-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           11.5.2-MariaDB - mariadb.org binary distribution
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour railtrip
CREATE DATABASE IF NOT EXISTS `railtrip` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;
USE `railtrip`;

-- Listage de la structure de la table railtrip. app_favori
CREATE TABLE IF NOT EXISTS `app_favori` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `roadtrip_id` int(11) NOT NULL,
  `utilisateur_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `App_favori_roadtrip_id_30a7f7b3_fk_App_roadtrip_id` (`roadtrip_id`),
  KEY `App_favori_utilisateur_id_eade7fc7_fk_App_utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `App_favori_roadtrip_id_30a7f7b3_fk_App_roadtrip_id` FOREIGN KEY (`roadtrip_id`) REFERENCES `app_roadtrip` (`id`),
  CONSTRAINT `App_favori_utilisateur_id_eade7fc7_fk_App_utilisateur_id` FOREIGN KEY (`utilisateur_id`) REFERENCES `app_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.app_favori : ~0 rows (environ)

-- Listage de la structure de la table railtrip. app_reaction
CREATE TABLE IF NOT EXISTS `app_reaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `like` tinyint(1) NOT NULL,
  `roadtrip_id` int(11) NOT NULL,
  `utilisateur_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `App_reaction_roadtrip_id_b17cd913_fk_App_roadtrip_id` (`roadtrip_id`),
  KEY `App_reaction_utilisateur_id_67a18bac_fk_App_utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `App_reaction_roadtrip_id_b17cd913_fk_App_roadtrip_id` FOREIGN KEY (`roadtrip_id`) REFERENCES `app_roadtrip` (`id`),
  CONSTRAINT `App_reaction_utilisateur_id_67a18bac_fk_App_utilisateur_id` FOREIGN KEY (`utilisateur_id`) REFERENCES `app_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.app_reaction : ~0 rows (environ)

-- Listage de la structure de la table railtrip. app_roadtrip
CREATE TABLE IF NOT EXISTS `app_roadtrip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `publique` tinyint(1) NOT NULL,
  `etapes` varchar(255) NOT NULL,
  `depart` date NOT NULL,
  `nbjour` int(11) NOT NULL,
  `description` varchar(255) NOT NULL,
  `utilisateur_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `App_roadtrip_utilisateur_id_a24145c1_fk_App_utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `App_roadtrip_utilisateur_id_a24145c1_fk_App_utilisateur_id` FOREIGN KEY (`utilisateur_id`) REFERENCES `app_utilisateur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.app_roadtrip : ~0 rows (environ)

-- Listage de la structure de la table railtrip. app_utilisateur
CREATE TABLE IF NOT EXISTS `app_utilisateur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mdp` varchar(128) NOT NULL,
  `pseudo` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pseudo` (`pseudo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.app_utilisateur : ~0 rows (environ)
INSERT INTO `app_utilisateur` (`id`, `mdp`, `pseudo`) VALUES
	(1, 'pbkdf2_sha256$870000$FFTkQPAXbu13NM0CU77xQz$hHFx3oP6qOvOsrjSNEG2CxU04Kk6mEzEUEoeqt8qG7U=', 'SPACE');

-- Listage de la structure de la table railtrip. auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.auth_group : ~0 rows (environ)

-- Listage de la structure de la table railtrip. auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.auth_group_permissions : ~0 rows (environ)

-- Listage de la structure de la table railtrip. auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.auth_permission : ~40 rows (environ)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add utilisateur', 7, 'add_utilisateur'),
	(26, 'Can change utilisateur', 7, 'change_utilisateur'),
	(27, 'Can delete utilisateur', 7, 'delete_utilisateur'),
	(28, 'Can view utilisateur', 7, 'view_utilisateur'),
	(29, 'Can add road trip', 8, 'add_roadtrip'),
	(30, 'Can change road trip', 8, 'change_roadtrip'),
	(31, 'Can delete road trip', 8, 'delete_roadtrip'),
	(32, 'Can view road trip', 8, 'view_roadtrip'),
	(33, 'Can add reaction', 9, 'add_reaction'),
	(34, 'Can change reaction', 9, 'change_reaction'),
	(35, 'Can delete reaction', 9, 'delete_reaction'),
	(36, 'Can view reaction', 9, 'view_reaction'),
	(37, 'Can add favori', 10, 'add_favori'),
	(38, 'Can change favori', 10, 'change_favori'),
	(39, 'Can delete favori', 10, 'delete_favori'),
	(40, 'Can view favori', 10, 'view_favori');

-- Listage de la structure de la table railtrip. auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.auth_user : ~0 rows (environ)

-- Listage de la structure de la table railtrip. auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.auth_user_groups : ~0 rows (environ)

-- Listage de la structure de la table railtrip. auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.auth_user_user_permissions : ~0 rows (environ)

-- Listage de la structure de la table railtrip. django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.django_admin_log : ~0 rows (environ)

-- Listage de la structure de la table railtrip. django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.django_content_type : ~10 rows (environ)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(10, 'App', 'favori'),
	(9, 'App', 'reaction'),
	(8, 'App', 'roadtrip'),
	(7, 'App', 'utilisateur'),
	(1, 'admin', 'logentry'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session');

-- Listage de la structure de la table railtrip. django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.django_migrations : ~19 rows (environ)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'App', '0001_initial', '2024-11-25 12:22:06.549478'),
	(2, 'contenttypes', '0001_initial', '2024-11-25 12:22:06.607986'),
	(3, 'auth', '0001_initial', '2024-11-25 12:22:07.053542'),
	(4, 'admin', '0001_initial', '2024-11-25 12:22:07.159808'),
	(5, 'admin', '0002_logentry_remove_auto_add', '2024-11-25 12:22:07.171396'),
	(6, 'admin', '0003_logentry_add_action_flag_choices', '2024-11-25 12:22:07.178944'),
	(7, 'contenttypes', '0002_remove_content_type_name', '2024-11-25 12:22:07.238503'),
	(8, 'auth', '0002_alter_permission_name_max_length', '2024-11-25 12:22:07.275091'),
	(9, 'auth', '0003_alter_user_email_max_length', '2024-11-25 12:22:07.296682'),
	(10, 'auth', '0004_alter_user_username_opts', '2024-11-25 12:22:07.304544'),
	(11, 'auth', '0005_alter_user_last_login_null', '2024-11-25 12:22:07.333817'),
	(12, 'auth', '0006_require_contenttypes_0002', '2024-11-25 12:22:07.333817'),
	(13, 'auth', '0007_alter_validators_add_error_messages', '2024-11-25 12:22:07.339945'),
	(14, 'auth', '0008_alter_user_username_max_length', '2024-11-25 12:22:07.364935'),
	(15, 'auth', '0009_alter_user_last_name_max_length', '2024-11-25 12:22:07.390356'),
	(16, 'auth', '0010_alter_group_name_max_length', '2024-11-25 12:22:07.409278'),
	(17, 'auth', '0011_update_proxy_permissions', '2024-11-25 12:22:07.414461'),
	(18, 'auth', '0012_alter_user_first_name_max_length', '2024-11-25 12:22:07.431269'),
	(19, 'sessions', '0001_initial', '2024-11-25 12:22:07.463209');

-- Listage de la structure de la table railtrip. django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- Listage des données de la table railtrip.django_session : ~2 rows (environ)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('8q0bcjie02rl5uichdruv7u3r68jw16k', 'eyJ1c2VyX2lkIjoxfQ:1tFaGw:aft_gGBtcdwRtWg2nwwObnhLAOUCWxga8Hp3qQGmX3Q', '2024-12-09 14:41:06.060259'),
	('n761aw7es8qstzkc6ec6c0ysamhtw045', 'eyJ1c2VyX2lkIjoxfQ:1tN8je:-Eb7YiUl9_33Jl3gpUZxdCE62KG5a4JKcsWNTx7GQDc', '2024-12-30 10:53:58.098115');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
