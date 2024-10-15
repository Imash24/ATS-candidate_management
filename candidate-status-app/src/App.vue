<template>
  <div id="app">
    <CandidateList />
  </div>
</template>

<script>
// Import the CandidateList component
import CandidateList from './components/CandidateList.vue'

export default {
  name: 'App',
  components: {
    CandidateList  // Register CandidateList as a component
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
