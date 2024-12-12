-- Insérer des utilisateurs dans `app_utilisateur`
INSERT INTO `app_utilisateur` (`id`, `mdp`, `pseudo`) VALUES
(4, MD5('password123'), 'john_doe'),
(2, MD5('password456'), 'jane_smith'),
(3, MD5('password789'), 'mark_brown');

-- Insérer des roadtrips dans `app_roadtrip`
INSERT INTO `app_roadtrip` (`id`, `publique`, `etapes`, `depart`, `nbjour`, `description`, `utilisateur_id`) VALUES
(1, 1, 'Bordeaux-Lyon-Marseille', '2024-12-22', 10, 'Découverte des grandes villes françaises', 1),
(2, 0, 'Lyon-Marseille-Amiens', '2025-01-02', 7, 'Découvrir la diversité des paysages et des cultures françaises à travers un roadtrip captivant reliant Lyon, Marseille et Amiens. Une aventure de 7 jours riche en découvertes culturelles, culinaires et naturelles', 2),
(3, 1, 'Toulouse-Montpellier-Nimes', '2025-01-01', 5, 'Roadtrip en bord de mer', 3);

-- Insérer des favoris dans `app_favori`
INSERT INTO `app_favori` (`id`, `roadtrip_id`, `utilisateur_id`) VALUES
(1, 1, 2),
(2, 3, 1),
(3, 2, 3);

-- Insérer des réactions dans `app_reaction`
INSERT INTO `app_reaction` (`id`, `like`, `roadtrip_id`, `utilisateur_id`) VALUES
(1, 1, 1, 2),
(2, 0, 2, 1),
(3, 1, 3, 3);

-- Insérer des groupes dans `auth_group`
INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'Admins'),
(2, 'Users'),
(3, 'Guests');

-- Insérer des permissions dans `auth_permission`
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(41, 'Can moderate roadtrip', 8, 'moderate_roadtrip');

-- Associer des permissions aux groupes dans `auth_group_permissions`
INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(1, 1, 41);

-- Associer des utilisateurs à des groupes dans `auth_user_groups`
INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3);

-- Ajouter des utilisateurs dans `auth_user`
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, MD5('adminpass'), '2024-12-01 12:00:00', 1, 'admin', 'Admin', 'User', 'admin@example.com', 1, 1, '2024-12-01 10:00:00'),
(2, MD5('userpass'), '2024-12-02 14:00:00', 0, 'user1', 'User1', 'Test', 'user1@example.com', 0, 1, '2024-12-02 10:00:00'),
(3, MD5('guestpass'), '2024-12-03 16:00:00', 0, 'guest', 'Guest', 'Test', 'guest@example.com', 0, 1, '2024-12-03 10:00:00');
