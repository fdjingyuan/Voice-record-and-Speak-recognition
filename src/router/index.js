import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import MainApp from '@/components/MainApp'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: MainApp
    }
    // },
    //  {
    //   path: 'test',
    //   name: 'HelloWorld2',
    //   component: HelloWorld2
    // }
  ]
})
