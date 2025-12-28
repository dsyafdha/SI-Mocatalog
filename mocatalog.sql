-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 28, 2025 at 07:02 PM
-- Server version: 8.0.43
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `movie_catalog`
--
CREATE DATABASE IF NOT EXISTS `movie_catalog` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `movie_catalog`;

-- --------------------------------------------------------

--
-- Table structure for table `film`
--

CREATE TABLE `film` (
  `id_film` int NOT NULL,
  `judul` varchar(150) DEFAULT NULL,
  `id_kategori` int DEFAULT NULL,
  `sinopsis` text,
  `tahun` int DEFAULT NULL,
  `poster` varchar(255) DEFAULT 'default.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `film`
--

INSERT INTO `film` (`id_film`, `judul`, `id_kategori`, `sinopsis`, `tahun`, `poster`) VALUES
(2, 'John Wick', 1, 'Pembunuh bayaran legendaris', 2014, 'john_wick.jpg'),
(3, 'Avengers Endgame', 1, 'Pertempuran terakhir Avengers', 2019, 'avengers_endgame.jpg'),
(4, 'Laskar Pelangi', 2, 'Perjuangan pendidikan anak desa', 2008, 'laskar_pelangi.jpg'),
(5, 'Forrest Gump', 2, 'Kisah hidup penuh makna', 1994, 'forrest_gump.jpg'),
(6, 'The Pursuit of Happyness', 2, 'Perjuangan seorang ayah', 2006, 'pursuit_of_happyness.jpg'),
(7, 'Mr Bean Holiday', 3, 'Liburan penuh kekonyolan', 2007, 'mr_beans_holiday.jpg'),
(8, 'Home Alone', 3, 'Anak kecil melawan pencuri', 1990, 'home_alone_.jpg'),
(9, 'The Hangover', 3, 'Petualangan gila', 2009, 'hangover.jpg'),
(10, 'The Conjuring', 4, 'Teror rumah angker', 2013, 'conjuring.jpg'),
(11, 'Insidious', 4, 'Teror dimensi lain', 2010, 'insidious.jpg'),
(12, 'IT', 4, 'Teror badut mengerikan', 2017, 'It.jpg'),
(13, 'Titanic', 5, 'Cinta di kapal mewah', 1997, 'titanic.jpg'),
(14, 'La La Land', 5, 'Cinta dan mimpi', 2016, 'la_la_land.jpg'),
(15, 'The Notebook', 5, 'Cinta sejati', 2004, 'notebook.jpg'),
(16, 'Gone Girl', 6, 'Istri menghilang', 2014, 'gone_girl_ver4.jpg'),
(17, 'Shutter Island', 6, 'Misteri rumah sakit jiwa', 2010, 'shutter_island.jpg'),
(18, 'Se7en', 6, 'Pembunuh berantai', 1995, 'seven.jpg'),
(19, 'Interstellar', 7, 'Misi luar angkasa', 2014, 'interstellar.jpg'),
(20, 'Inception', 7, 'Mimpi dalam mimpi', 2010, 'inception.jpg'),
(21, 'Avatar', 7, 'Planet Pandora', 2009, 'avatar.jpg'),
(22, 'Harry Potter', 8, 'Dunia sihir', 2001, 'harry_potter_and_the_sorcerers_stone.jpg'),
(23, 'Lord of the Rings', 8, 'Cincin kekuasaan', 2001, 'lord_of_the_rings.jpg'),
(24, 'Toy Story', 9, 'Mainan hidup', 1995, 'toy_story.jpg'),
(25, 'Up', 9, 'Petualangan balon', 2009, 'up.jpg'),
(34, 'The Raid', 1, 'Polisi melakukan penggerebekan', 2011, 'the_raid.jpg'),
(37, 'The Exorcist', 4, 'Gadis kecil yang kerasukan iblis jahat', 1973, 'exorcist.jpg'),
(38, 'Evil Dead Rise', 4, 'Penemuan kitab orang mati di apartemen', 2023, 'evil_dead_rise.jpg'),
(39, 'A Nightmare on Elm Street', 4, 'Teror pembunuh di dalam mimpi', 1984, 'nightmare_on_elm_street.jpg'),
(40, 'Jujutsu Kaisen 0', 9, 'Kisah kutukan cinta yang sangat kuat', 2021, 'jujutsu_kaisen_zero.jpg'),
(41, 'Weathering With You', 9, 'Gadis yang bisa mengendalikan cuaca', 2019, 'weathering_with_you.jpg'),
(42, 'Harry Potter and the Chamber of Secrets', 8, 'Misteri kamar rahasia di Hogwarts', 2002, 'harry_potter_and_the_chamber_of_secrets.jpg'),
(43, 'Harry Potter and the Prisoner of Azkaban', 8, 'Pelarian tawanan berbahaya dari penjara sihir', 2004, 'harry_potter_and_the_prisoner_of_azkaban.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `kategori_film`
--

CREATE TABLE `kategori_film` (
  `id_kategori` int NOT NULL,
  `nama_kategori` varchar(100) DEFAULT NULL,
  `deskripsi` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `kategori_film`
--

INSERT INTO `kategori_film` (`id_kategori`, `nama_kategori`, `deskripsi`) VALUES
(1, 'Action', 'Film penuh adegan aksi'),
(2, 'Drama', 'Cerita emosional dan kehidupan'),
(3, 'Comedy', 'Film dengan unsur humor'),
(4, 'Horror', 'Film bertema horor dan ketegangan'),
(5, 'Romance', 'Cerita percintaan'),
(6, 'Thriller', 'Film penuh misteri'),
(7, 'Sci-Fi', 'Fiksi ilmiah dan futuristik'),
(8, 'Fantasy', 'Dunia imajinatif'),
(9, 'Animation', 'Film animasi'),
(10, 'Adventure', 'Petualangan seru');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_user` int NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` text,
  `role` enum('admin','user') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id_user`, `username`, `password`, `role`) VALUES
(1, 'admin', 'scrypt:32768:8:1$b52UlXgpF28eSV7l$d389773c242f45233899a4eba8598b549eb3c8043b1b0da0c6f0c6f3fc3bfee67792bd9346eae3e767e1cf00679667d331600b2171749fcf680944d8f7fc7355', 'admin'),
(8, 'user', 'scrypt:32768:8:1$AF4yxPTn8f4iakd0$f27eb8d6186c21706cc70e1be3946d32952ac4077a09019e2e93b5a1ea16ac61b306187d3c5723657e66e31177e549abca3b4d3e483de95d3bc1d83c45322936', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `watchlist`
--

CREATE TABLE `watchlist` (
  `id_watchlist` int NOT NULL,
  `id_user` int DEFAULT NULL,
  `id_film` int DEFAULT NULL,
  `status` enum('Belum Ditonton','Sudah Ditonton') DEFAULT 'Belum Ditonton'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `watchlist`
--

INSERT INTO `watchlist` (`id_watchlist`, `id_user`, `id_film`, `status`) VALUES
(28, 1, 25, 'Belum Ditonton'),
(29, 1, 25, 'Belum Ditonton');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `film`
--
ALTER TABLE `film`
  ADD PRIMARY KEY (`id_film`),
  ADD KEY `id_kategori` (`id_kategori`);

--
-- Indexes for table `kategori_film`
--
ALTER TABLE `kategori_film`
  ADD PRIMARY KEY (`id_kategori`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- Indexes for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD PRIMARY KEY (`id_watchlist`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `id_film` (`id_film`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `film`
--
ALTER TABLE `film`
  MODIFY `id_film` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `kategori_film`
--
ALTER TABLE `kategori_film`
  MODIFY `id_kategori` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `watchlist`
--
ALTER TABLE `watchlist`
  MODIFY `id_watchlist` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `film`
--
ALTER TABLE `film`
  ADD CONSTRAINT `film_ibfk_1` FOREIGN KEY (`id_kategori`) REFERENCES `kategori_film` (`id_kategori`);

--
-- Constraints for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD CONSTRAINT `watchlist_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`),
  ADD CONSTRAINT `watchlist_ibfk_2` FOREIGN KEY (`id_film`) REFERENCES `film` (`id_film`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
