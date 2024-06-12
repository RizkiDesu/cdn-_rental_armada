/** @odoo-module **/
import { registry } from '@web/core/registry';

const {
    Component,
    onMounted,
    onWillUnmount,
    useRef,
} = owl;

export class NamaKomponen extends Component {
    /** @type {String} */
    static template = 'nama_modul.NamaKomponen';

    /** @type {HTMLElement} */
    #element_1;

    setup() {
        super.setup();

        this.#element_1 = useRef('element_1');

        onMounted(this.#onMounted);
        onWillUnmount(this.#onWillUnmount);

    }

    #onMounted() {

    }

    #onWillUnmount() {
    }
}

registry.category('fields').add('component_or_tag_name', NamaKomponen);
