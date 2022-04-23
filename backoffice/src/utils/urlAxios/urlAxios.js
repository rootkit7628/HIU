import Axios from 'axios';

const uRI = "https://hiu-api.iteam-s.mg/hiu-auth"

const RouteAxios = Axios.create({
    baseURL: uRI 
})

export {
    RouteAxios, uRI
}
