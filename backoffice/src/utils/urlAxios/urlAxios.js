import Axios from 'axios';

const uRI = "https://hiu-api.iteam-s.mg/api/v1"

const RouteAxios = Axios.create({
    baseURL: uRI 
})

export {
    RouteAxios, uRI
}
