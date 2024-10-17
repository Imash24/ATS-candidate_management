<template>
  <div id="app">
    <CandidateList />
  </div>
</template>

<script>
import CandidateList from './components/CandidateList.vue';

export default {
  components: {
    CandidateList
  }
};
</script>

<style>
/* Global styles */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
