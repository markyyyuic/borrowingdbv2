-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 25, 2024 at 04:52 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `web2_grp0`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(1, 'Groceries'),
(2, 'Utilities'),
(3, 'Entertainment'),
(4, 'Dining'),
(5, 'Transportation'),
(6, 'Healthcare'),
(7, 'Clothing'),
(8, 'Education'),
(9, 'Travel'),
(10, 'Miscellaneous');

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

CREATE TABLE `expenses` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`id`, `user_id`, `category_id`, `amount`, `description`, `date`) VALUES
(1, 1, 1, 83.24, 'Expense for Groceries', '2024-01-30'),
(2, 1, 1, 96.32, 'Expense for Groceries', '2024-02-21'),
(3, 1, 1, 80.90, 'Expense for Groceries', '2024-02-07'),
(4, 1, 1, 70.21, 'Expense for Groceries', '2024-02-07'),
(5, 1, 1, 5.82, 'Expense for Groceries', '2024-02-14'),
(6, 2, 1, 78.67, 'Expense for Groceries', '2024-02-03'),
(7, 2, 1, 42.35, 'Expense for Groceries', '2024-01-31'),
(8, 2, 1, 96.72, 'Expense for Groceries', '2024-02-17'),
(9, 2, 1, 56.48, 'Expense for Groceries', '2024-01-28'),
(10, 2, 1, 2.66, 'Expense for Groceries', '2024-02-16'),
(11, 3, 1, 42.14, 'Expense for Groceries', '2024-02-19'),
(12, 3, 1, 76.77, 'Expense for Groceries', '2024-02-19'),
(13, 3, 1, 79.42, 'Expense for Groceries', '2024-02-16'),
(14, 3, 1, 17.95, 'Expense for Groceries', '2024-01-28'),
(15, 3, 1, 26.38, 'Expense for Groceries', '2024-02-12'),
(16, 4, 1, 39.71, 'Expense for Groceries', '2024-02-05'),
(17, 4, 1, 17.09, 'Expense for Groceries', '2024-01-31'),
(18, 4, 1, 67.32, 'Expense for Groceries', '2024-01-31'),
(19, 4, 1, 25.30, 'Expense for Groceries', '2024-02-04'),
(20, 4, 1, 74.80, 'Expense for Groceries', '2024-02-06'),
(21, 5, 1, 93.59, 'Expense for Groceries', '2024-02-02'),
(22, 5, 1, 4.98, 'Expense for Groceries', '2024-01-28'),
(23, 5, 1, 52.25, 'Expense for Groceries', '2024-02-01'),
(24, 5, 1, 47.92, 'Expense for Groceries', '2024-01-27'),
(25, 5, 1, 40.16, 'Expense for Groceries', '2024-02-22'),
(26, 7, 1, 31.80, 'Expense for Groceries', '2024-02-17'),
(27, 7, 1, 42.78, 'Expense for Groceries', '2024-02-16'),
(28, 7, 1, 26.54, 'Expense for Groceries', '2024-02-14'),
(29, 7, 1, 19.36, 'Expense for Groceries', '2024-02-02'),
(30, 7, 1, 28.98, 'Expense for Groceries', '2024-02-22'),
(31, 1, 2, 76.29, 'Expense for Utilities', '2024-02-12'),
(32, 1, 2, 88.65, 'Expense for Utilities', '2024-02-22'),
(33, 1, 2, 97.70, 'Expense for Utilities', '2024-02-10'),
(34, 1, 2, 58.46, 'Expense for Utilities', '2024-02-13'),
(35, 1, 2, 31.54, 'Expense for Utilities', '2024-02-15'),
(36, 2, 2, 72.99, 'Expense for Utilities', '2024-02-06'),
(37, 2, 2, 3.01, 'Expense for Utilities', '2024-02-19'),
(38, 2, 2, 0.33, 'Expense for Utilities', '2024-02-15'),
(39, 2, 2, 79.10, 'Expense for Utilities', '2024-01-30'),
(40, 2, 2, 0.04, 'Expense for Utilities', '2024-02-14'),
(41, 3, 2, 88.76, 'Expense for Utilities', '2024-02-16'),
(42, 3, 2, 86.11, 'Expense for Utilities', '2024-02-14'),
(43, 3, 2, 37.16, 'Expense for Utilities', '2024-02-05'),
(44, 3, 2, 31.17, 'Expense for Utilities', '2024-02-10'),
(45, 3, 2, 57.75, 'Expense for Utilities', '2024-02-14'),
(46, 4, 2, 16.67, 'Expense for Utilities', '2024-02-05'),
(47, 4, 2, 96.98, 'Expense for Utilities', '2024-02-02'),
(48, 4, 2, 92.62, 'Expense for Utilities', '2024-02-16'),
(49, 4, 2, 87.01, 'Expense for Utilities', '2024-02-15'),
(50, 4, 2, 19.54, 'Expense for Utilities', '2024-01-30'),
(51, 5, 2, 88.15, 'Expense for Utilities', '2024-02-04'),
(52, 5, 2, 98.92, 'Expense for Utilities', '2024-02-03'),
(53, 5, 2, 86.25, 'Expense for Utilities', '2024-02-25'),
(54, 5, 2, 48.35, 'Expense for Utilities', '2024-02-14'),
(55, 5, 2, 42.43, 'Expense for Utilities', '2024-01-27'),
(56, 7, 2, 71.11, 'Expense for Utilities', '2024-02-09'),
(57, 7, 2, 69.25, 'Expense for Utilities', '2024-02-02'),
(58, 7, 2, 75.73, 'Expense for Utilities', '2024-02-11'),
(59, 7, 2, 15.71, 'Expense for Utilities', '2024-02-16'),
(60, 7, 2, 16.84, 'Expense for Utilities', '2024-01-31'),
(61, 1, 3, 78.51, 'Expense for Entertainment', '2024-02-15'),
(62, 1, 3, 40.23, 'Expense for Entertainment', '2024-01-28'),
(63, 1, 3, 57.68, 'Expense for Entertainment', '2024-02-25'),
(64, 1, 3, 33.81, 'Expense for Entertainment', '2024-02-06'),
(65, 1, 3, 23.35, 'Expense for Entertainment', '2024-02-19'),
(66, 2, 3, 39.39, 'Expense for Entertainment', '2024-02-16'),
(67, 2, 3, 38.28, 'Expense for Entertainment', '2024-01-27'),
(68, 2, 3, 72.80, 'Expense for Entertainment', '2024-02-04'),
(69, 2, 3, 38.59, 'Expense for Entertainment', '2024-02-02'),
(70, 2, 3, 78.03, 'Expense for Entertainment', '2024-02-09'),
(71, 3, 3, 35.25, 'Expense for Entertainment', '2024-02-21'),
(72, 3, 3, 67.41, 'Expense for Entertainment', '2024-01-29'),
(73, 3, 3, 63.64, 'Expense for Entertainment', '2024-02-14'),
(74, 3, 3, 2.41, 'Expense for Entertainment', '2024-01-28'),
(75, 3, 3, 73.11, 'Expense for Entertainment', '2024-02-02'),
(76, 4, 3, 67.32, 'Expense for Entertainment', '2024-02-24'),
(77, 4, 3, 21.18, 'Expense for Entertainment', '2024-01-29'),
(78, 4, 3, 96.49, 'Expense for Entertainment', '2024-02-24'),
(79, 4, 3, 42.61, 'Expense for Entertainment', '2024-01-28'),
(80, 4, 3, 41.21, 'Expense for Entertainment', '2024-02-18'),
(81, 5, 3, 99.42, 'Expense for Entertainment', '2024-02-19'),
(82, 5, 3, 18.14, 'Expense for Entertainment', '2024-02-19'),
(83, 5, 3, 49.84, 'Expense for Entertainment', '2024-01-31'),
(84, 5, 3, 83.74, 'Expense for Entertainment', '2024-02-08'),
(85, 5, 3, 42.52, 'Expense for Entertainment', '2024-02-15'),
(86, 7, 3, 54.24, 'Expense for Entertainment', '2024-02-07'),
(87, 7, 3, 47.86, 'Expense for Entertainment', '2024-02-10'),
(88, 7, 3, 21.19, 'Expense for Entertainment', '2024-02-11'),
(89, 7, 3, 71.93, 'Expense for Entertainment', '2024-02-20'),
(90, 7, 3, 75.85, 'Expense for Entertainment', '2024-02-18'),
(91, 1, 4, 93.73, 'Expense for Dining', '2024-01-28'),
(92, 1, 4, 98.34, 'Expense for Dining', '2024-02-24'),
(93, 1, 4, 24.85, 'Expense for Dining', '2024-02-22'),
(94, 1, 4, 87.03, 'Expense for Dining', '2024-01-27'),
(95, 1, 4, 29.88, 'Expense for Dining', '2024-02-09'),
(96, 2, 4, 84.46, 'Expense for Dining', '2024-02-08'),
(97, 2, 4, 35.77, 'Expense for Dining', '2024-02-24'),
(98, 2, 4, 19.55, 'Expense for Dining', '2024-02-01'),
(99, 2, 4, 49.55, 'Expense for Dining', '2024-02-25'),
(100, 2, 4, 65.42, 'Expense for Dining', '2024-02-20'),
(101, 3, 4, 97.01, 'Expense for Dining', '2024-02-17'),
(102, 3, 4, 54.46, 'Expense for Dining', '2024-01-31'),
(103, 3, 4, 61.61, 'Expense for Dining', '2024-02-10'),
(104, 3, 4, 80.41, 'Expense for Dining', '2024-02-13'),
(105, 3, 4, 73.31, 'Expense for Dining', '2024-02-14'),
(106, 4, 4, 69.30, 'Expense for Dining', '2024-02-16'),
(107, 4, 4, 56.86, 'Expense for Dining', '2024-01-31'),
(108, 4, 4, 56.71, 'Expense for Dining', '2024-02-17'),
(109, 4, 4, 65.72, 'Expense for Dining', '2024-02-11'),
(110, 4, 4, 38.29, 'Expense for Dining', '2024-02-10'),
(111, 5, 4, 35.99, 'Expense for Dining', '2024-02-17'),
(112, 5, 4, 39.31, 'Expense for Dining', '2024-02-23'),
(113, 5, 4, 22.90, 'Expense for Dining', '2024-01-29'),
(114, 5, 4, 81.31, 'Expense for Dining', '2024-02-15'),
(115, 5, 4, 38.82, 'Expense for Dining', '2024-01-31'),
(116, 7, 4, 5.80, 'Expense for Dining', '2024-02-03'),
(117, 7, 4, 60.83, 'Expense for Dining', '2024-02-02'),
(118, 7, 4, 3.54, 'Expense for Dining', '2024-01-31'),
(119, 7, 4, 19.84, 'Expense for Dining', '2024-02-13'),
(120, 7, 4, 45.08, 'Expense for Dining', '2024-02-25'),
(121, 1, 5, 77.95, 'Expense for Transportation', '2024-02-01'),
(122, 1, 5, 75.34, 'Expense for Transportation', '2024-02-16'),
(123, 1, 5, 29.95, 'Expense for Transportation', '2024-02-09'),
(124, 1, 5, 90.92, 'Expense for Transportation', '2024-01-31'),
(125, 1, 5, 57.91, 'Expense for Transportation', '2024-02-16'),
(126, 2, 5, 82.04, 'Expense for Transportation', '2024-02-20'),
(127, 2, 5, 37.57, 'Expense for Transportation', '2024-02-14'),
(128, 2, 5, 75.52, 'Expense for Transportation', '2024-02-06'),
(129, 2, 5, 96.69, 'Expense for Transportation', '2024-01-30'),
(130, 2, 5, 57.47, 'Expense for Transportation', '2024-02-20'),
(131, 3, 5, 21.75, 'Expense for Transportation', '2024-02-10'),
(132, 3, 5, 95.97, 'Expense for Transportation', '2024-02-19'),
(133, 3, 5, 27.74, 'Expense for Transportation', '2024-02-05'),
(134, 3, 5, 63.24, 'Expense for Transportation', '2024-02-23'),
(135, 3, 5, 51.92, 'Expense for Transportation', '2024-02-15'),
(136, 4, 5, 17.41, 'Expense for Transportation', '2024-02-01'),
(137, 4, 5, 63.54, 'Expense for Transportation', '2024-02-05'),
(138, 4, 5, 50.46, 'Expense for Transportation', '2024-02-11'),
(139, 4, 5, 86.96, 'Expense for Transportation', '2024-01-29'),
(140, 4, 5, 98.15, 'Expense for Transportation', '2024-02-21'),
(141, 5, 5, 82.17, 'Expense for Transportation', '2024-02-06'),
(142, 5, 5, 77.91, 'Expense for Transportation', '2024-01-28'),
(143, 5, 5, 40.82, 'Expense for Transportation', '2024-02-20'),
(144, 5, 5, 74.26, 'Expense for Transportation', '2024-02-22'),
(145, 5, 5, 43.67, 'Expense for Transportation', '2024-02-02'),
(146, 7, 5, 61.28, 'Expense for Transportation', '2024-02-04'),
(147, 7, 5, 71.25, 'Expense for Transportation', '2024-02-13'),
(148, 7, 5, 2.18, 'Expense for Transportation', '2024-02-01'),
(149, 7, 5, 0.17, 'Expense for Transportation', '2024-02-08'),
(150, 7, 5, 83.62, 'Expense for Transportation', '2024-02-11'),
(151, 1, 6, 87.31, 'Expense for Healthcare', '2024-01-28'),
(152, 1, 6, 6.29, 'Expense for Healthcare', '2024-02-10'),
(153, 1, 6, 33.63, 'Expense for Healthcare', '2024-02-21'),
(154, 1, 6, 82.38, 'Expense for Healthcare', '2024-02-07'),
(155, 1, 6, 62.55, 'Expense for Healthcare', '2024-02-17'),
(156, 2, 6, 46.99, 'Expense for Healthcare', '2024-02-09'),
(157, 2, 6, 29.79, 'Expense for Healthcare', '2024-01-31'),
(158, 2, 6, 43.21, 'Expense for Healthcare', '2024-02-09'),
(159, 2, 6, 52.82, 'Expense for Healthcare', '2024-01-28'),
(160, 2, 6, 14.76, 'Expense for Healthcare', '2024-01-30'),
(161, 3, 6, 5.11, 'Expense for Healthcare', '2024-02-09'),
(162, 3, 6, 64.23, 'Expense for Healthcare', '2024-02-09'),
(163, 3, 6, 74.33, 'Expense for Healthcare', '2024-02-22'),
(164, 3, 6, 34.14, 'Expense for Healthcare', '2024-02-15'),
(165, 3, 6, 79.79, 'Expense for Healthcare', '2024-01-30'),
(166, 4, 6, 8.76, 'Expense for Healthcare', '2024-02-03'),
(167, 4, 6, 48.28, 'Expense for Healthcare', '2024-02-21'),
(168, 4, 6, 38.48, 'Expense for Healthcare', '2024-02-13'),
(169, 4, 6, 96.54, 'Expense for Healthcare', '2024-02-09'),
(170, 4, 6, 88.05, 'Expense for Healthcare', '2024-02-03'),
(171, 5, 6, 4.07, 'Expense for Healthcare', '2024-01-27'),
(172, 5, 6, 84.83, 'Expense for Healthcare', '2024-02-18'),
(173, 5, 6, 75.24, 'Expense for Healthcare', '2024-01-27'),
(174, 5, 6, 66.13, 'Expense for Healthcare', '2024-02-15'),
(175, 5, 6, 79.22, 'Expense for Healthcare', '2024-01-30'),
(176, 7, 6, 10.02, 'Expense for Healthcare', '2024-02-01'),
(177, 7, 6, 77.45, 'Expense for Healthcare', '2024-02-13'),
(178, 7, 6, 81.27, 'Expense for Healthcare', '2024-02-02'),
(179, 7, 6, 47.20, 'Expense for Healthcare', '2024-02-25'),
(180, 7, 6, 65.31, 'Expense for Healthcare', '2024-02-19'),
(181, 1, 7, 16.03, 'Expense for Clothing', '2024-02-22'),
(182, 1, 7, 16.79, 'Expense for Clothing', '2024-02-12'),
(183, 1, 7, 74.84, 'Expense for Clothing', '2024-02-14'),
(184, 1, 7, 70.84, 'Expense for Clothing', '2024-02-14'),
(185, 1, 7, 72.40, 'Expense for Clothing', '2024-02-10'),
(186, 2, 7, 38.08, 'Expense for Clothing', '2024-02-14'),
(187, 2, 7, 71.85, 'Expense for Clothing', '2024-02-11'),
(188, 2, 7, 22.51, 'Expense for Clothing', '2024-02-05'),
(189, 2, 7, 80.94, 'Expense for Clothing', '2024-01-28'),
(190, 2, 7, 35.36, 'Expense for Clothing', '2024-01-30'),
(191, 3, 7, 43.44, 'Expense for Clothing', '2024-02-11'),
(192, 3, 7, 7.05, 'Expense for Clothing', '2024-01-29'),
(193, 3, 7, 43.01, 'Expense for Clothing', '2024-02-15'),
(194, 3, 7, 53.80, 'Expense for Clothing', '2024-02-08'),
(195, 3, 7, 35.17, 'Expense for Clothing', '2024-01-27'),
(196, 4, 7, 84.02, 'Expense for Clothing', '2024-02-18'),
(197, 4, 7, 79.78, 'Expense for Clothing', '2024-02-20'),
(198, 4, 7, 59.66, 'Expense for Clothing', '2024-02-14'),
(199, 4, 7, 15.53, 'Expense for Clothing', '2024-02-07'),
(200, 4, 7, 58.13, 'Expense for Clothing', '2024-02-23'),
(201, 5, 7, 64.72, 'Expense for Clothing', '2024-02-25'),
(202, 5, 7, 6.42, 'Expense for Clothing', '2024-02-16'),
(203, 5, 7, 39.59, 'Expense for Clothing', '2024-02-25'),
(204, 5, 7, 94.38, 'Expense for Clothing', '2024-02-06'),
(205, 5, 7, 36.92, 'Expense for Clothing', '2024-01-29'),
(206, 7, 7, 52.04, 'Expense for Clothing', '2024-02-01'),
(207, 7, 7, 56.44, 'Expense for Clothing', '2024-02-15'),
(208, 7, 7, 4.07, 'Expense for Clothing', '2024-02-21'),
(209, 7, 7, 69.38, 'Expense for Clothing', '2024-01-27'),
(210, 7, 7, 81.49, 'Expense for Clothing', '2024-02-21'),
(211, 1, 8, 23.93, 'Expense for Education', '2024-02-02'),
(212, 1, 8, 21.21, 'Expense for Education', '2024-02-04'),
(213, 1, 8, 87.61, 'Expense for Education', '2024-02-17'),
(214, 1, 8, 73.68, 'Expense for Education', '2024-01-31'),
(215, 1, 8, 11.54, 'Expense for Education', '2024-01-27'),
(216, 2, 8, 56.02, 'Expense for Education', '2024-01-31'),
(217, 2, 8, 60.58, 'Expense for Education', '2024-02-12'),
(218, 2, 8, 46.89, 'Expense for Education', '2024-01-27'),
(219, 2, 8, 45.65, 'Expense for Education', '2024-02-15'),
(220, 2, 8, 45.44, 'Expense for Education', '2024-02-20'),
(221, 3, 8, 52.39, 'Expense for Education', '2024-02-23'),
(222, 3, 8, 86.44, 'Expense for Education', '2024-02-24'),
(223, 3, 8, 70.79, 'Expense for Education', '2024-02-15'),
(224, 3, 8, 67.14, 'Expense for Education', '2024-02-17'),
(225, 3, 8, 38.46, 'Expense for Education', '2024-02-23'),
(226, 4, 8, 26.59, 'Expense for Education', '2024-02-23'),
(227, 4, 8, 59.11, 'Expense for Education', '2024-02-04'),
(228, 4, 8, 83.76, 'Expense for Education', '2024-02-25'),
(229, 4, 8, 59.51, 'Expense for Education', '2024-01-29'),
(230, 4, 8, 76.73, 'Expense for Education', '2024-02-22'),
(231, 5, 8, 22.35, 'Expense for Education', '2024-02-01'),
(232, 5, 8, 34.16, 'Expense for Education', '2024-02-16'),
(233, 5, 8, 47.82, 'Expense for Education', '2024-02-11'),
(234, 5, 8, 1.10, 'Expense for Education', '2024-02-08'),
(235, 5, 8, 90.47, 'Expense for Education', '2024-02-03'),
(236, 7, 8, 9.10, 'Expense for Education', '2024-02-20'),
(237, 7, 8, 58.66, 'Expense for Education', '2024-02-13'),
(238, 7, 8, 32.62, 'Expense for Education', '2024-02-14'),
(239, 7, 8, 91.79, 'Expense for Education', '2024-02-12'),
(240, 7, 8, 50.40, 'Expense for Education', '2024-02-21'),
(241, 1, 9, 31.60, 'Expense for Travel', '2024-02-23'),
(242, 1, 9, 46.78, 'Expense for Travel', '2024-02-23'),
(243, 1, 9, 4.36, 'Expense for Travel', '2024-01-28'),
(244, 1, 9, 61.76, 'Expense for Travel', '2024-02-18'),
(245, 1, 9, 34.23, 'Expense for Travel', '2024-01-27'),
(246, 2, 9, 94.63, 'Expense for Travel', '2024-02-03'),
(247, 2, 9, 89.78, 'Expense for Travel', '2024-02-18'),
(248, 2, 9, 54.27, 'Expense for Travel', '2024-01-27'),
(249, 2, 9, 23.10, 'Expense for Travel', '2024-02-18'),
(250, 2, 9, 50.39, 'Expense for Travel', '2024-02-01'),
(251, 3, 9, 49.57, 'Expense for Travel', '2024-02-23'),
(252, 3, 9, 88.24, 'Expense for Travel', '2024-02-20'),
(253, 3, 9, 30.38, 'Expense for Travel', '2024-01-28'),
(254, 3, 9, 83.02, 'Expense for Travel', '2024-02-16'),
(255, 3, 9, 3.92, 'Expense for Travel', '2024-02-17'),
(256, 4, 9, 27.26, 'Expense for Travel', '2024-02-10'),
(257, 4, 9, 82.74, 'Expense for Travel', '2024-02-09'),
(258, 4, 9, 26.69, 'Expense for Travel', '2024-02-05'),
(259, 4, 9, 62.54, 'Expense for Travel', '2024-02-23'),
(260, 4, 9, 48.05, 'Expense for Travel', '2024-02-20'),
(261, 5, 9, 50.11, 'Expense for Travel', '2024-01-28'),
(262, 5, 9, 19.58, 'Expense for Travel', '2024-02-21'),
(263, 5, 9, 21.03, 'Expense for Travel', '2024-02-08'),
(264, 5, 9, 23.32, 'Expense for Travel', '2024-02-12'),
(265, 5, 9, 53.79, 'Expense for Travel', '2024-02-15'),
(266, 7, 9, 12.16, 'Expense for Travel', '2024-02-08'),
(267, 7, 9, 47.01, 'Expense for Travel', '2024-02-06'),
(268, 7, 9, 83.66, 'Expense for Travel', '2024-02-18'),
(269, 7, 9, 66.41, 'Expense for Travel', '2024-02-07'),
(270, 7, 9, 8.90, 'Expense for Travel', '2024-02-08'),
(271, 1, 10, 71.44, 'Expense for Miscellaneous', '2024-02-02'),
(272, 1, 10, 77.17, 'Expense for Miscellaneous', '2024-02-10'),
(273, 1, 10, 23.36, 'Expense for Miscellaneous', '2024-02-06'),
(274, 1, 10, 49.25, 'Expense for Miscellaneous', '2024-02-09'),
(275, 1, 10, 25.46, 'Expense for Miscellaneous', '2024-02-06'),
(276, 2, 10, 40.50, 'Expense for Miscellaneous', '2024-02-22'),
(277, 2, 10, 40.31, 'Expense for Miscellaneous', '2024-02-06'),
(278, 2, 10, 1.39, 'Expense for Miscellaneous', '2024-02-21'),
(279, 2, 10, 63.57, 'Expense for Miscellaneous', '2024-02-02'),
(280, 2, 10, 95.39, 'Expense for Miscellaneous', '2024-02-12'),
(281, 3, 10, 40.21, 'Expense for Miscellaneous', '2024-02-06'),
(282, 3, 10, 5.44, 'Expense for Miscellaneous', '2024-02-16'),
(283, 3, 10, 41.54, 'Expense for Miscellaneous', '2024-02-22'),
(284, 3, 10, 40.27, 'Expense for Miscellaneous', '2024-02-07'),
(285, 3, 10, 91.23, 'Expense for Miscellaneous', '2024-02-05'),
(286, 4, 10, 71.03, 'Expense for Miscellaneous', '2024-02-11'),
(287, 4, 10, 28.43, 'Expense for Miscellaneous', '2024-01-27'),
(288, 4, 10, 0.92, 'Expense for Miscellaneous', '2024-02-22'),
(289, 4, 10, 61.65, 'Expense for Miscellaneous', '2024-02-05'),
(290, 4, 10, 63.13, 'Expense for Miscellaneous', '2024-02-23'),
(291, 5, 10, 44.63, 'Expense for Miscellaneous', '2024-02-25'),
(292, 5, 10, 79.70, 'Expense for Miscellaneous', '2024-01-29'),
(293, 5, 10, 12.60, 'Expense for Miscellaneous', '2024-01-29'),
(294, 5, 10, 22.07, 'Expense for Miscellaneous', '2024-02-15'),
(295, 5, 10, 5.96, 'Expense for Miscellaneous', '2024-02-18'),
(296, 7, 10, 14.63, 'Expense for Miscellaneous', '2024-01-28'),
(297, 7, 10, 24.37, 'Expense for Miscellaneous', '2024-02-13'),
(298, 7, 10, 31.25, 'Expense for Miscellaneous', '2024-02-15'),
(299, 7, 10, 74.38, 'Expense for Miscellaneous', '2024-02-04'),
(300, 7, 10, 32.10, 'Expense for Miscellaneous', '2024-02-11');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`) VALUES
(1, 'user1', '*668425423DB5193AF921380129F465A6425216D0', 'user1@example.com'),
(2, 'user2', '*DC52755F3C09F5923046BD42AFA76BD1D80DF2E9', 'user2@example.com'),
(3, 'user3', '*40C3E7D386A2FADBDF69ACEBE7AA4DC3C723D798', 'user3@example.com'),
(4, 'user4', '*F97AEB38B3275C06D822FC9341A2151642C81988', 'user4@example.com'),
(5, 'user5', '*5A6AB0B9E84ED1EEC9E8AE9C926922C5D1EDF908', 'user5@example.com'),
(7, 'user7', '$2b$12$Q1c7A/z5H2YvkNRVvHlcier1nmXGrkVOTmlkg4t6G6QuZHM3UNpkq', 'user7@example.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `expenses`
--
ALTER TABLE `expenses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=512;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `expenses`
--
ALTER TABLE `expenses`
  ADD CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `expenses_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
