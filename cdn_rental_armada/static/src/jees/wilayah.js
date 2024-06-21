/** @odoo-module **/
import { registry } from '@web/core/registry';
import rpc from 'web.rpc';
// import { useState } from '@odoo/owl/hooks';

const {
    Component,
    onMounted,
    onWillUnmount,
    useRef,
    useState
} = owl;


export class WilayahWidget extends Component {
  /** @type {String} */
  static template = 'WilayahWidget';

  /** @type {HTMLElement} */
  #provinsi;
  #kota;
  #kecamatan;
  #desa;

  setup() {
    super.setup();
    var propsval = this.props.value != '' ? JSON.parse(this.props.value) : ''
    this.state = useState({
      provinsi  : [],
      kota      : [],
      kecamatan : [],
      desa      : [],
      props: {
        provinsi  : propsval != '' ? propsval.provinsi : {},
        kota      : propsval != '' ? propsval.kota : {},
        kecamatan : propsval != '' ? propsval.kecamatan : {},
        desa      : propsval != '' ? propsval.desa : {},
      }
    });

    onMounted(async () => {
        this.state.provinsi = await this.fetchProvinces();
    });
    this.#provinsi = useRef('provinsi-select');
    this.#kota = useRef('kota-select');
    this.#kecamatan = useRef('kecamatan-select');
    this.#desa = useRef('desa-select');

    if(propsval != ''){
      this.fetchkota(this.state.props.provinsi.id);
      this.fetchKecamatan(this.state.props.kota.id);
      this.fetchDesa(this.state.props.kecamatan.id);
    }

  }

  _onChangeProvinsi(event) {
    const selectedProvinceId = this.#provinsi.el.value;
    this.state.kota = []
    this.state.kecamatan = []
    this.state.desa = []
    this.state.props.kota = {}
    this.state.props.kecamatan = {}
    this.state.props.desa = {}
    this.fetchkota(selectedProvinceId);

    // set props value
    this.state.props.provinsi.id = this.#provinsi.el.value;
    this.state.props.provinsi.name = this.#provinsi.el.options[this.#provinsi.el.selectedIndex].text;
    
    this.props.update(JSON.stringify(this.state.props))
  }
  _onChangeKota(event) {
    const selectedKotaId = this.#kota.el.value;
    this.state.kecamatan = []
    this.state.desa = []
    this.state.props.kecamatan = {}
    this.state.props.desa = {}
    this.fetchKecamatan(selectedKotaId);

    // set props value
    this.state.props.kota.id = this.#kota.el.value;
    this.state.props.kota.name = this.#kota.el.options[this.#kota.el.selectedIndex].text;
    
    this.props.update(JSON.stringify(this.state.props))
  }
  _onChangeKecamatan(event) {
    const selectedKecamatanId = this.#kecamatan.el.value;
    this.state.desa = []
    this.state.props.desa = {}
    this.fetchDesa(selectedKecamatanId);

    // set props value
    this.state.props.kecamatan.id = this.#kecamatan.el.value;
    this.state.props.kecamatan.name = this.#kecamatan.el.options[this.#kecamatan.el.selectedIndex].text;
    
    this.props.update(JSON.stringify(this.state.props))
  }
  _onChangeDesa(event) {
    // set props value
    this.state.props.desa.id = this.#desa.el.value;
    this.state.props.desa.name = this.#desa.el.options[this.#desa.el.selectedIndex].text;
    
    this.props.update(JSON.stringify(this.state.props))
  }

  async fetchProvinces() {
    try {
        const response = await fetch('/provinsi-api', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        

        return data;
    } catch (error) {
        console.error('Error fetching provinces:', error);
        return [];
    }
  }

  async fetchkota(id_provinsi) {
    try {
        const response = await fetch('/kota-api?provinsi_id='+id_provinsi, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        this.state.kota = data;
        return [];
    } catch (error) {
        console.error('Error fetching provinces:', error);
        return [];
    }
  }

  async fetchKecamatan(id_kota) {
    try {
        const response = await fetch('/kecamatan-api?kota_id='+id_kota, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.state.kecamatan = data;
        return [];
    } catch (error) {
        console.error('Error fetching provinces:', error);
        return [];
    }
  }

  async fetchDesa(id_kecamatan) {
    try {
        const response = await fetch('/desa-api?kecamatan_id='+id_kecamatan, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.state.desa = data;
        return [];
    } catch (error) {
        console.error('Error fetching provinces:', error);
        return [];
    }
  }
}

registry.category('fields').add('wilayah_widget', WilayahWidget);