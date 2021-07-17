import Vue from 'vue';
import VueRouter from 'vue-router';
import Ping from '../components/Ping.vue';
import Books from '../components/Books.vue';
import Papers from '../components/Papers.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
  {
    path: '/books',
    name: 'Books',
    component: Books,
  },
  {
    path: '/papers',
    name: 'Papers',
    component: Papers,
  },

];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
