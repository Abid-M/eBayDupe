import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/Auction',name:'Auction',component: () => import('../views/Auction.vue')},
    {path:'/Product/:data', name:'Product', component: () => import('../views/Product.vue')},
    {path:'/Profile', name:'Profile',component: () => import('../views/Profile.vue')},
    {path:'/', name:'Homepage',component: () => import('../views/Homepage.vue')},
  ]
})

export default router
