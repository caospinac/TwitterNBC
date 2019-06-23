const axios = require('axios');

export default class Util {

    constructor() {
        this.ajax = this.ajax.bind(this);
        this.getCookie = this.getCookie.bind(this);
    }

    getCookie(name) {
        var r = document.cookie.match(/\b/ + name + /=([^;]*)\b/);
        return r ? r[1] : undefined;
    }

    ajax(request){
        var url = request.url,
            method = request.method || "GET",
            data = request.data || {},
            params = request.params || {},
            contentType;

        if (method === "POST" || method === "PUT") {
            contentType = "application/json";
        } else {
            contentType = "application/x-www-form-urlencoded; charset=UTF-8";
        }

        return axios({
            url: url,
            headers: {
                Pragma: 'no-cache',
                'X-XSRFToken': this.getCookie('_xsrf')
            },
            cache: false,
            data: data,
            params: params,
            method: method,
            dataType: "json",
            contentType: contentType
        });
    }
}
