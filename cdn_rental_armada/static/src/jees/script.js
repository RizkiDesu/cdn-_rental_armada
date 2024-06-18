odoo.define('cdn_rental_armada.jees', function (require) {
    "use strict"

    var rpc = require('web.rpc')

    // ----------------------------------------asal ----------------------------------------

    function filterKotaByProvinsi(provinsi_id) {
        var $kotaSelect = document.getElementById('kota')
        $kotaSelect.innerHTML = ''
        $kotaSelect.append(new Option('', ''))  // Tambahkan opsi kosong

        rpc.query({
            route: '/get_kota_by_provinsi',
            params: { 'provinsi_id': provinsi_id }
        }).then(function(data) {
            data.kota.forEach(function(kota) {
                var option = new Option(kota.name, kota.id)
                $kotaSelect.append(option)
            })
        })
    }

    function filterKecamatanByKota(kota_id) {
        var $kecamatanSelect = document.getElementById('kecamatan');
        $kecamatanSelect.innerHTML = ''
        $kecamatanSelect.append(new Option('', ''))

        rpc.query({
            route: '/get_kecamatan_by_kota',
            params: { 'kota_id': kota_id }
        }).then(function(data) {
            data.kecamatan.forEach(function(kecamatan) {
                var option = new Option(kecamatan.name, kecamatan.id)
                $kecamatanSelect.append(option)
            });
        });
    }

    function filterDesaByKecamatan(kecamatan_id) {
        var $desaSelect = document.getElementById('desa')
        $desaSelect.innerHTML = ''
        $desaSelect.append(new Option('', ''))
        rpc.query({
            route: '/get_desa_by_kecamatan',
            params: { 'kecamatan_id': kecamatan_id }
        }).then(function(data) {
            data.desa.forEach(function(desa) {
                var option = new Option(desa.name, desa.id)
                $desaSelect.append(option)
            })
        })
    }

// ----------------------------------------tujuan ----------------------------------------

    function filterKotaByProvinsiTujuan(provinsi_id) {
        var $kotaSelect = document.getElementById('kota_tujuan')
        $kotaSelect.innerHTML = ''
        $kotaSelect.append(new Option('', ''))

        rpc.query({
            route: '/get_kota_by_provinsi_tujuan',
            params: { 'provinsi_id': provinsi_id }
        }).then(function(data) {
            data.kota.forEach(function(kota) {
                var option = new Option(kota.name, kota.id)
                $kotaSelect.append(option)
            })
        })
    }
    function filterKecamatanByKotaTujuan(kota_id) {
        var $kecamatanSelect = document.getElementById('kecamatan_tujuan')
        $kecamatanSelect.innerHTML = ''
        $kecamatanSelect.append(new Option('', ''))

        rpc.query({
            route: '/get_kecamatan_by_kota_tujuan',
            params: { 'kota_id': kota_id }
        }).then(function(data) {
            data.kecamatan.forEach(function(kecamatan) {
                var option = new Option(kecamatan.name, kecamatan.id)
                $kecamatanSelect.append(option)
            })
        })
    }

    function filterDesaByKecamatanTujuan(kecamatan_id) {
        var $desaSelect = document.getElementById('desa_tujuan')
        $desaSelect.innerHTML = '' 
        $desaSelect.append(new Option('', ''))  

        rpc.query({
            route: '/get_desa_by_kecamatan_tujuan',
            params: { 'kecamatan_id': kecamatan_id }
        }).then(function(data) {
            data.desa.forEach(function(desa) {
                var option = new Option(desa.name, desa.id)
                $desaSelect.append(option)
            })
        })
    }


// ---------------------------------------- PRODUCT ----------------------------------------
    function filterProdukByJenisArmada(jenis_armada) {
        var $produkSelect = document.getElementById('produk')
        $produkSelect.selectedIndex = 0;
        $produkSelect.selectedIndex = ''
        $produkSelect.innerHTML = ''  
        $produkSelect.append(new Option('', '')) 

        rpc.query({
            route: '/get_produk_by_jenis_armada',
            params: { 'jenis_armada': jenis_armada }
        }).then(function(data) {
            data.produk.forEach(function(produk) {
                
                var option = new Option(produk.name, produk.id)
                $produkSelect.append(option)
            })
        })
    }

    function tampilkanHargaProduct(product_id) {
        // console.log(product_id)
        var $harga = document.getElementById('harga')
        $harga.innerHTML = ''  // Kosongkan pilihan harga yang ada
        rpc.query({
            route: '/get_harga_by_product',
            params: { 'product_id': product_id }
        }
        ).then(function(data) {
            // $harga.innerHTML = ''
            $harga.innerHTML = data.harga
            total()
        })
        // return product_id
    }

    function total() {
        let harga = document.getElementById('harga').innerHTML
        let jumlah = document.getElementById('jmlh').value
        let durasi = document.getElementById('durasi').value

        let total = document.getElementById('total')
        total.innerHTML = ''
        total.innerHTML = harga * jumlah * durasi
    }

    

    // function total (jumlah, product_id) {
        
    //     total = document.getElementById('total')
    //     total.innerHTML = ''
    //     rpc.query({
    //         route: '/get_harga_by_product',
    //         params: { 'product_id': product_id }
    //     }).then(function(data) {
    //         total.innerHTML = data.harga * jumlah
    //     })

        
    // }
    window.total                        = total
    window.tampilkanHargaProduct        = tampilkanHargaProduct
    window.filterProdukByJenisArmada    = filterProdukByJenisArmada

    window.filterKotaByProvinsi         = filterKotaByProvinsi
    window.filterKecamatanByKota        = filterKecamatanByKota
    window.filterDesaByKecamatan        = filterDesaByKecamatan

    window.filterKotaByProvinsiTujuan   = filterKotaByProvinsiTujuan
    window.filterKecamatanByKotaTujuan  = filterKecamatanByKotaTujuan
    window.filterDesaByKecamatanTujuan  = filterDesaByKecamatanTujuan
});

