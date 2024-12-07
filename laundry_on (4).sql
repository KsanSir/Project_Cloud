-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 07, 2024 at 10:57 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `laundry_on`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin1'),
(2, 'user1', 'password1');

-- --------------------------------------------------------

--
-- Table structure for table `jenis_paket`
--

CREATE TABLE `jenis_paket` (
  `jenis_laundry` varchar(10) NOT NULL,
  `harga` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jenis_paket`
--

INSERT INTO `jenis_paket` (`jenis_laundry`, `harga`) VALUES
('EXPRESS', 10000),
('KILAT', 10000),
('REGULER', 5000);

-- --------------------------------------------------------

--
-- Table structure for table `karyawan`
--

CREATE TABLE `karyawan` (
  `id_karyawan` varchar(4) NOT NULL,
  `kode_karyawan` varchar(2) NOT NULL,
  `nama` varchar(35) NOT NULL,
  `kontak` varchar(15) DEFAULT NULL,
  `alamat` varchar(30) NOT NULL,
  `jam_kerja` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `karyawan`
--

INSERT INTO `karyawan` (`id_karyawan`, `kode_karyawan`, `nama`, `kontak`, `alamat`, `jam_kerja`) VALUES
('A01', 'A', 'Aditya', '087654327890', 'Condongcatur, Depok, Sleman', 7),
('A02', 'A', 'Maftuh', '089212345678', 'Mancasan Lor', 6),
('A03', 'A', 'Muza', '083838202066', 'Condongcatur', 6),
('B01', 'B', 'Alvin', '076512340909', 'Yogyakarta, Sleman', 4),
('B02', 'B', 'Hana', '089212345678', 'Sleman', 6),
('C01', 'C', 'Kevin', '084523450001', 'Mancasan Lor', 7);

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

CREATE TABLE `pelanggan` (
  `id_pelanggan` int(4) UNSIGNED ZEROFILL NOT NULL,
  `nama` varchar(35) NOT NULL,
  `alamat` varchar(50) DEFAULT NULL,
  `kontak` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pelanggan`
--

INSERT INTO `pelanggan` (`id_pelanggan`, `nama`, `alamat`, `kontak`) VALUES
(0026, 'Rikii', 'Sleman', '089712345432'),
(0027, 'fiero', 'pajangan', '087568945623'),
(0028, 'Tina', 'bantul', '087956312549'),
(0029, 'pratama', 'babarsari', '087412563987'),
(0030, 'ibnu', 'seturan', '087451236987'),
(0031, 'andreas', 'tambak boyo', '087456932587'),
(0032, 'semar', 'candi kebang', '081365478923'),
(0033, 'nur', 'congcat', '087956842398'),
(0034, 'putri', 'maguwo', '085487623458'),
(0035, 'fakih', 'jakal', '087956874138'),
(0036, 'Indra', 'Gunung Kidul', '081323242237'),
(0037, 'adit', 'Jl klalin', '08131414269142');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id_nota` varchar(15) NOT NULL,
  `id_pelanggan` int(4) UNSIGNED ZEROFILL NOT NULL,
  `jenis_laundry` varchar(10) NOT NULL,
  `berat` int(2) NOT NULL,
  `tanggal_masuk` datetime NOT NULL,
  `tanggal_keluar` date DEFAULT NULL,
  `id_karyawan` varchar(35) NOT NULL,
  `status` varchar(10) NOT NULL,
  `status_pembayaran` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`id_nota`, `id_pelanggan`, `jenis_laundry`, `berat`, `tanggal_masuk`, `tanggal_keluar`, `id_karyawan`, `status`, `status_pembayaran`) VALUES
('001E210624', 0027, 'EXPRESS', 0, '2024-06-14 10:30:00', '2024-06-22', 'B02', 'SELESAI', 'LUNAS'),
('001K210624', 0029, 'KILAT', 0, '2024-06-16 18:00:00', NULL, 'B01', 'DITERIMA', 'BELUM BAYAR'),
('001R210624', 0026, 'REGULER', 5, '2024-06-21 01:44:00', '2024-06-22', 'B01', 'SELESAI', 'LUNAS'),
('002E210624', 0029, 'EXPRESS', 2, '2024-06-21 13:33:00', NULL, 'A03', 'DITERIMA', 'BELUM BAYAR'),
('002K210624', 0030, 'KILAT', 4, '2024-06-17 16:33:00', NULL, 'B02', 'DITERIMA', 'LUNAS'),
('002R210624', 0028, 'REGULER', 0, '2024-06-18 10:20:00', NULL, 'C01', 'DITERIMA', 'LUNAS'),
('003E210624', 0032, 'EXPRESS', 5, '2024-06-20 13:37:00', NULL, 'B01', 'DITERIMA', 'LUNAS'),
('003K210624', 0031, 'KILAT', 3, '2024-06-19 08:34:00', NULL, 'A03', 'DITERIMA', 'BELUM BAYAR'),
('003R210624', 0034, 'REGULER', 10, '2024-06-17 15:39:00', NULL, 'B01', 'DITERIMA', 'BELUM BAYAR'),
('004E210624', 0036, 'EXPRESS', 4, '2024-06-21 16:54:00', '2024-06-22', 'B01', 'SELESAI', 'LUNAS'),
('004K210624', 0033, 'KILAT', 6, '2024-06-19 10:45:00', NULL, 'C01', 'DITERIMA', 'LUNAS'),
('001E071224', 0026, 'EXPRESS', 1, '2024-12-07 16:14:00', NULL, 'B02', 'DITERIMA', 'LUNAS'),
('001K071224', 0027, 'KILAT', 2, '2024-12-07 16:18:00', NULL, 'A02', 'DITERIMA', 'BELUM BAYAR'),
('001R071224', 0029, 'REGULER', 3, '2024-12-07 16:23:00', NULL, 'A02', 'DITERIMA', 'BELUM BAYAR'),
('002E071224', 0029, 'EXPRESS', 3, '2024-12-07 16:25:00', NULL, 'A02', 'DITERIMA', 'LUNAS'),
('003E071224', 0028, 'EXPRESS', 3, '2024-12-07 16:29:00', NULL, 'A01', 'DITERIMA', 'BELUM BAYAR'),
('002R071224', 0030, 'REGULER', 10, '2024-12-07 16:38:00', NULL, 'B02', 'DITERIMA', 'LUNAS');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `jenis_paket`
--
ALTER TABLE `jenis_paket`
  ADD PRIMARY KEY (`jenis_laundry`);

--
-- Indexes for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD PRIMARY KEY (`id_karyawan`),
  ADD KEY `kode_karyawan` (`kode_karyawan`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`id_pelanggan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `id_pelanggan` int(4) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD CONSTRAINT `kode_karyawan` FOREIGN KEY (`kode_karyawan`) REFERENCES `posisi` (`kode_karyawan`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
