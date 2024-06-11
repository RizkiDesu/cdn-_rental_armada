odoo.define('cdn_rental_armada.location_filter', function (require) {
    "use strict";

    var rpc = require('web.rpc')

    // ----------------------------------------asal ----------------------------------------

    function filterKotaByProvinsi(provinsi_id) {
        var $kotaSelect = document.getElementById('kota')
        $kotaSelect.innerHTML = '';  // Kosongkan pilihan kota yang ada
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
        $kecamatanSelect.innerHTML = '';  // Kosongkan pilihan kecamatan yang ada
        $kecamatanSelect.append(new Option('', '')) // Tambahkan opsi kosong

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
        $desaSelect.innerHTML = ''  // Kosongkan pilihan desa yang ada
        $desaSelect.append(new Option('', ''))  // Tambahkan opsi kosong

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
        $kotaSelect.innerHTML = ''  // Kosongkan pilihan kota yang ada
        $kotaSelect.append(new Option('', ''))  // Tambahkan opsi kosong

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
        $kecamatanSelect.innerHTML = ''  // Kosongkan pilihan kecamatan yang ada
        $kecamatanSelect.append(new Option('', ''))  // Tambahkan opsi kosong

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
        $desaSelect.innerHTML = ''  // Kosongkan pilihan desa yang ada
        $desaSelect.append(new Option('', ''))  // Tambahkan opsi kosong

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

    window.filterKotaByProvinsi         = filterKotaByProvinsi
    window.filterKecamatanByKota        = filterKecamatanByKota
    window.filterDesaByKecamatan        = filterDesaByKecamatan

    window.filterKotaByProvinsiTujuan   = filterKotaByProvinsiTujuan
    window.filterKecamatanByKotaTujuan  = filterKecamatanByKotaTujuan
    window.filterDesaByKecamatanTujuan  = filterDesaByKecamatanTujuan
});

