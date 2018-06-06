import Vue from 'vue'
import Router from 'vue-router'
//import MainApp from '@/components/MainApp'
import Recorder from '@/components/Recorder'
Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path: '/',
    //   name: 'index',
    //   component: MainApp
    // }


     {
      path: '/',
      name: 'test',
      component:Recorder
    }
  ]
})
