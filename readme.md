# CDN Armada Rental 
## [database](https://drive.google.com/drive/folders/1Z-ypLgJ2T4i7Lo7Mz6paKM47maQ1jrlY?usp=sharing)

## Master Data

### Armada :

- Jenis Armada (selection)

- Bis Pariwisata

- Travel : HiAce, Elf, Long Elf

- Mobil : Inova, Avanza, APV, Grandmax

- Tahun Pembuatan

- Plat No

- No Rangka & No Mesin

### Supir --> inherits : res.partner

- SIM dan Masa Berlaku sd

### Kernet / Tenaga bantu  --> inherits : res.partner

### Product : product.product

- Sewa Pariwisata (Armada + Supir)

- Sewa Armada saja

- Service Charge

- UoM = hari

## Transaksi

### Booking / Penyewaan Armada --> Create Invoicemencatat : Jenis Sewa, Tujuan, Armada, Supir, Tenaga Bantu, Durasi Sewa

- Pembayaran Sewa

## Perawatan Armada

- Uji KIR

- Service Rutin

## Informasi / Laporan

- Armada tersedia (berdasarkan Jenis)

- Surat Booking
