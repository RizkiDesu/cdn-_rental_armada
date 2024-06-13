/** @odoo-module **/
import { registry } from '@web/core/registry';
// import { useState } from '@odoo/owl/hooks';

const {
    Component,
    onMounted,
    onWillUnmount,
    useRef,
    useState
} = owl;


export class Peta extends Component {
    /** @type {String} */
    static template = 'PetaArmada';

    /** @type {HTMLElement} */
    #map_container;
    #map;

    setup() {
      super.setup();
      var propsval = this.props.value != '' ? JSON.parse(this.props.value.replace(/'/g, '"')) : {'lat' : '-7.975229131435001', 'lng' : '112.63040852567805'}
      this.state = useState({ 
        lat: propsval.lat,
        lng: propsval.lng
      });
      this.#map_container = useRef('map_container');

      onMounted(this.#onMounted);
      onWillUnmount(this.#onWillUnmount);

    }

    #onMounted() {
      this.#map = L.map(this.#map_container.el, {
         center: [this.state.lat, this.state.lng],
         zoom: 13
      });
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
      }).addTo(this.#map);
      
      var marker;
      if (marker) {
        marker.setLatLng([this.state.lat, this.state.lng]);
      } else {
        marker = L.marker([this.state.lat, this.state.lng]).addTo(this.#map);
      }
      this.#map.on('click', (e) => {
          var lat = e.latlng.lat;
          var lng = e.latlng.lng;
          this.state.lat = lat;
          this.state.lng = lng;
          marker.setLatLng(e.latlng);
          this.props.update(e.latlng)
          
      });
      
    }

    #onWillUnmount() {
      this.#map.remove();
    }
}

// Peta.template = 'cdn_rental_armada.Peta';
registry.category('fields').add('peta_widget', Peta);
// core.form_widget_registry.add('peta_widget',Peta);
