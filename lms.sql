-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 21, 2020 at 06:18 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lms`
--

-- --------------------------------------------------------

--
-- Table structure for table `author`
--

CREATE TABLE `author` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `author`
--

INSERT INTO `author` (`id`, `name`) VALUES
(1, 'Titu Andresscu'),
(2, 'Sergei Milownsky'),
(3, 'Yamuna Sir'),
(4, 'Satyadev Sir'),
(5, 'Jinwala Sir');

-- --------------------------------------------------------

--
-- Table structure for table `book`
--

CREATE TABLE `book` (
  `id` int(11) NOT NULL,
  `isbn` int(11) DEFAULT NULL,
  `arrival` varchar(255) DEFAULT NULL,
  `del` varchar(255) DEFAULT 'Not'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `book`
--

INSERT INTO `book` (`id`, `isbn`, `arrival`, `del`) VALUES
(1, 11111, '2020-07-08', 'Not'),
(2, 11111, '2020-07-08', 'Not'),
(3, 12345, '2020-07-09', 'Not'),
(4, 12345, '2020-07-10', 'Not');

-- --------------------------------------------------------

--
-- Table structure for table `book_author`
--

CREATE TABLE `book_author` (
  `id` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  `book_isbn` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `book_author`
--

INSERT INTO `book_author` (`id`, `author_id`, `book_isbn`) VALUES
(1, 1, 11111),
(2, 1, 12345),
(4, 2, 11111),
(5, 3, 10000),
(6, 4, 10000);

-- --------------------------------------------------------

--
-- Table structure for table `book_borrow`
--

CREATE TABLE `book_borrow` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `issue` varchar(255) DEFAULT NULL,
  `deposit` varchar(255) DEFAULT 'Not'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `book_borrow`
--

INSERT INTO `book_borrow` (`id`, `user_id`, `book_id`, `issue`, `deposit`) VALUES
(4, 18, 1, '2020-07-11', '2020-07-11'),
(5, 18, 1, '2020-07-11', '2020-07-15'),
(8, 18, 1, '2020-07-20', '2020-07-20'),
(9, 18, 2, '2020-07-20', '2020-07-20');

-- --------------------------------------------------------

--
-- Table structure for table `book_edition`
--

CREATE TABLE `book_edition` (
  `isbn` int(11) NOT NULL,
  `publisher_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `pages` int(11) DEFAULT NULL,
  `discipline` enum('CSE','ME','CE','Math','Phy','EE','Hindi') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `book_edition`
--

INSERT INTO `book_edition` (`isbn`, `publisher_id`, `title`, `pages`, `discipline`) VALUES
(10000, 2, 'CV', 100, 'CSE'),
(11111, 2, 'Discrete Math', 100, 'CSE'),
(12345, 2, 'Optics', 500, 'Phy'),
(13333, 3, 'Hands on ML', 800, 'CSE');

-- --------------------------------------------------------

--
-- Table structure for table `book_tags`
--

CREATE TABLE `book_tags` (
  `id` int(11) NOT NULL,
  `book_isbn` int(11) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `book_tags`
--

INSERT INTO `book_tags` (`id`, `book_isbn`, `tag_id`) VALUES
(1, 11111, 4),
(2, 10000, 4);

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `id` int(11) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `paper`
--

CREATE TABLE `paper` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `periodical_isbn` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `paper`
--

INSERT INTO `paper` (`id`, `name`, `periodical_isbn`) VALUES
(1, 'Recent Advances in Fabrics', 12121),
(2, 'Electrons', 12121);

-- --------------------------------------------------------

--
-- Table structure for table `paper_author`
--

CREATE TABLE `paper_author` (
  `id` int(11) NOT NULL,
  `author_id` int(11) DEFAULT NULL,
  `paper_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `paper_author`
--

INSERT INTO `paper_author` (`id`, `author_id`, `paper_id`) VALUES
(1, 4, 1),
(2, 2, 1),
(3, 3, 2);

-- --------------------------------------------------------

--
-- Table structure for table `periodical`
--

CREATE TABLE `periodical` (
  `id` int(11) NOT NULL,
  `isbn` int(11) DEFAULT NULL,
  `arrival` varchar(255) DEFAULT NULL,
  `del` varchar(255) DEFAULT 'Not'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `periodical`
--

INSERT INTO `periodical` (`id`, `isbn`, `arrival`, `del`) VALUES
(1, 12121, '2020-07-09', 'Not'),
(2, 12121, '2020-07-09', 'Not'),
(3, 12121, '2020-07-11', 'Not');

-- --------------------------------------------------------

--
-- Table structure for table `periodical_borrow`
--

CREATE TABLE `periodical_borrow` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `periodical_id` int(11) DEFAULT NULL,
  `issue` varchar(255) DEFAULT NULL,
  `deposit` varchar(255) DEFAULT 'Not'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `periodical_edition`
--

CREATE TABLE `periodical_edition` (
  `isbn` int(11) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `volume` int(11) DEFAULT NULL,
  `publisher_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `periodical_edition`
--

INSERT INTO `periodical_edition` (`isbn`, `year`, `volume`, `publisher_id`, `title`) VALUES
(12121, 1990, 1, 3, 'Advancement in fabrics');

-- --------------------------------------------------------

--
-- Table structure for table `periodical_tags`
--

CREATE TABLE `periodical_tags` (
  `id` int(11) NOT NULL,
  `periodical_id` int(11) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `publisher`
--

CREATE TABLE `publisher` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `publisher`
--

INSERT INTO `publisher` (`id`, `name`) VALUES
(2, 'A'),
(3, 'B');

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE `tag` (
  `id` int(11) NOT NULL,
  `value` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tag`
--

INSERT INTO `tag` (`id`, `value`) VALUES
(1, 'mystery'),
(2, 'thriller'),
(3, 'light'),
(4, 'academia'),
(5, 'comic');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `user_type` enum('Students','Faculty','Staff','Guest') DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `paid` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `user_type`, `password`, `paid`) VALUES
(16, 'ee', 'e@e', 'ee', 'Faculty', '12', 0),
(18, 'aa', 'aa@aa', 'aa', 'Faculty', '1234', 0),
(21, 'Rajesh', 'rajesh@gmail.com', 'Rajesh', 'Staff', '1234', 0),
(23, 'Test User', 'test@gmail.com', 'Test User', 'Guest', '1234', 0);

-- --------------------------------------------------------

--
-- Table structure for table `user_info`
--

CREATE TABLE `user_info` (
  `user_type` varchar(255) NOT NULL,
  `book_limit` int(11) DEFAULT NULL,
  `day_limit` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_info`
--

INSERT INTO `user_info` (`user_type`, `book_limit`, `day_limit`) VALUES
('Faculty', 6, 30),
('Guest', 2, 7),
('Staff', 4, 30),
('Students', 3, 15);

-- --------------------------------------------------------

--
-- Table structure for table `waiting`
--

CREATE TABLE `waiting` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `book_isbn` int(11) DEFAULT NULL,
  `request` varchar(255) DEFAULT 'Not'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `waiting`
--

INSERT INTO `waiting` (`id`, `user_id`, `book_isbn`, `request`) VALUES
(1, 18, 11111, '2020-07-11');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `author`
--
ALTER TABLE `author`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`id`),
  ADD KEY `isbn` (`isbn`);

--
-- Indexes for table `book_author`
--
ALTER TABLE `book_author`
  ADD PRIMARY KEY (`id`),
  ADD KEY `author_id` (`author_id`),
  ADD KEY `book_isbn` (`book_isbn`);

--
-- Indexes for table `book_borrow`
--
ALTER TABLE `book_borrow`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `book_edition`
--
ALTER TABLE `book_edition`
  ADD PRIMARY KEY (`isbn`),
  ADD KEY `publisher_id` (`publisher_id`);

--
-- Indexes for table `book_tags`
--
ALTER TABLE `book_tags`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_isbn` (`book_isbn`),
  ADD KEY `tag_id` (`tag_id`);

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `paper`
--
ALTER TABLE `paper`
  ADD PRIMARY KEY (`id`),
  ADD KEY `periodical_isbn` (`periodical_isbn`);

--
-- Indexes for table `paper_author`
--
ALTER TABLE `paper_author`
  ADD PRIMARY KEY (`id`),
  ADD KEY `author_id` (`author_id`),
  ADD KEY `paper_id` (`paper_id`);

--
-- Indexes for table `periodical`
--
ALTER TABLE `periodical`
  ADD PRIMARY KEY (`id`),
  ADD KEY `isbn` (`isbn`);

--
-- Indexes for table `periodical_borrow`
--
ALTER TABLE `periodical_borrow`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `periodical_id` (`periodical_id`);

--
-- Indexes for table `periodical_edition`
--
ALTER TABLE `periodical_edition`
  ADD PRIMARY KEY (`isbn`),
  ADD KEY `publisher_id` (`publisher_id`);

--
-- Indexes for table `periodical_tags`
--
ALTER TABLE `periodical_tags`
  ADD PRIMARY KEY (`id`),
  ADD KEY `periodical_id` (`periodical_id`),
  ADD KEY `tag_id` (`tag_id`);

--
-- Indexes for table `publisher`
--
ALTER TABLE `publisher`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_info`
--
ALTER TABLE `user_info`
  ADD PRIMARY KEY (`user_type`);

--
-- Indexes for table `waiting`
--
ALTER TABLE `waiting`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_isbn` (`book_isbn`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `author`
--
ALTER TABLE `author`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `book`
--
ALTER TABLE `book`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `book_author`
--
ALTER TABLE `book_author`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `book_borrow`
--
ALTER TABLE `book_borrow`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `book_edition`
--
ALTER TABLE `book_edition`
  MODIFY `isbn` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13334;

--
-- AUTO_INCREMENT for table `book_tags`
--
ALTER TABLE `book_tags`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `message`
--
ALTER TABLE `message`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `paper`
--
ALTER TABLE `paper`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `paper_author`
--
ALTER TABLE `paper_author`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `periodical`
--
ALTER TABLE `periodical`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `periodical_borrow`
--
ALTER TABLE `periodical_borrow`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `periodical_tags`
--
ALTER TABLE `periodical_tags`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `publisher`
--
ALTER TABLE `publisher`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tag`
--
ALTER TABLE `tag`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `waiting`
--
ALTER TABLE `waiting`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `book`
--
ALTER TABLE `book`
  ADD CONSTRAINT `book_ibfk_1` FOREIGN KEY (`isbn`) REFERENCES `book_edition` (`isbn`);

--
-- Constraints for table `book_author`
--
ALTER TABLE `book_author`
  ADD CONSTRAINT `book_author_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`),
  ADD CONSTRAINT `book_author_ibfk_2` FOREIGN KEY (`book_isbn`) REFERENCES `book_edition` (`isbn`);

--
-- Constraints for table `book_borrow`
--
ALTER TABLE `book_borrow`
  ADD CONSTRAINT `book_borrow_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `book_borrow_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`);

--
-- Constraints for table `book_edition`
--
ALTER TABLE `book_edition`
  ADD CONSTRAINT `book_edition_ibfk_1` FOREIGN KEY (`publisher_id`) REFERENCES `publisher` (`id`);

--
-- Constraints for table `book_tags`
--
ALTER TABLE `book_tags`
  ADD CONSTRAINT `book_tags_ibfk_1` FOREIGN KEY (`book_isbn`) REFERENCES `book_edition` (`isbn`),
  ADD CONSTRAINT `book_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`);

--
-- Constraints for table `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `message_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `paper`
--
ALTER TABLE `paper`
  ADD CONSTRAINT `paper_ibfk_1` FOREIGN KEY (`periodical_isbn`) REFERENCES `periodical` (`isbn`);

--
-- Constraints for table `paper_author`
--
ALTER TABLE `paper_author`
  ADD CONSTRAINT `paper_author_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`),
  ADD CONSTRAINT `paper_author_ibfk_2` FOREIGN KEY (`paper_id`) REFERENCES `paper` (`id`);

--
-- Constraints for table `periodical`
--
ALTER TABLE `periodical`
  ADD CONSTRAINT `periodical_ibfk_1` FOREIGN KEY (`isbn`) REFERENCES `periodical_edition` (`isbn`);

--
-- Constraints for table `periodical_borrow`
--
ALTER TABLE `periodical_borrow`
  ADD CONSTRAINT `periodical_borrow_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `periodical_borrow_ibfk_2` FOREIGN KEY (`periodical_id`) REFERENCES `periodical` (`id`);

--
-- Constraints for table `periodical_edition`
--
ALTER TABLE `periodical_edition`
  ADD CONSTRAINT `periodical_edition_ibfk_1` FOREIGN KEY (`publisher_id`) REFERENCES `publisher` (`id`);

--
-- Constraints for table `periodical_tags`
--
ALTER TABLE `periodical_tags`
  ADD CONSTRAINT `periodical_tags_ibfk_1` FOREIGN KEY (`periodical_id`) REFERENCES `periodical` (`id`),
  ADD CONSTRAINT `periodical_tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`);

--
-- Constraints for table `waiting`
--
ALTER TABLE `waiting`
  ADD CONSTRAINT `waiting_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `waiting_ibfk_2` FOREIGN KEY (`book_isbn`) REFERENCES `book_edition` (`isbn`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
