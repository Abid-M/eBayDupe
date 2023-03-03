<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>

  <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <div class="container">
      <a href="http://localhost:5173/" class="navbar-brand">Welcome to the Fake eBay</a>

      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navmenu"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navmenu">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/"><a href="#" class="nav-link">Home</a></router-link>
          </li>
          <li class="nav-item">
            <router-link to="/Auction"><a href="#" class="nav-link">Create Auction</a></router-link>
          </li>

          <li class="nav-tem">
            <router-link to="/Profile"><a href="#" class="nav-link">Profile</a></router-link>
          </li>

          <li class="nav-tem">
            <u><a href="http://localhost:8000/auctionapp/logout/" class="nav-link">Logout</a></u>
          </li>

        </ul>
      </div>
    </div>
  </nav>
<router-view/>    
</template>
<router-view/>

<style scoped>
.logo {
height: 6em;
padding: 1.5em;
will-change: filter;
}
.logo:hover {
filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
filter: drop-shadow(0 0 2em #42b883aa);
}
</style>


