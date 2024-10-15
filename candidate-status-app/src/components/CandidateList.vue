<template>
    <div class="container">
      <header>
        <h1>Candidate List</h1>
        <p>Manage candidate statuses by selecting or rejecting them below.</p>
      </header>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="candidate in candidates" :key="candidate.id">
            <td>{{ candidate.id }}</td>
            <td>{{ candidate.name }}</td>
            <td>{{ candidate.email }}</td>
            <td>
              <span :class="{'status-selected': candidate.status === 'selected', 'status-rejected': candidate.status === 'rejected'}">
                {{ candidate.status }}
              </span>
            </td>
            <td>
              <button class="btn btn-select" @click="updateStatus(candidate.id, 'selected')">Select</button>
              <button class="btn btn-reject" @click="updateStatus(candidate.id, 'rejected')">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        candidates: []
      };
    },
    created() {
      this.fetchCandidates();
    },
    methods: {
      fetchCandidates() {
        axios
          .get('http://127.0.0.1:5000/candidates')  // Backend Flask API
          .then(response => {
            this.candidates = response.data.candidates;
          })
          .catch(error => {
            console.log("Error fetching candidates:", error);
          });
      },
      updateStatus(id, status) {
        axios
          .post(`http://127.0.0.1:5000/update_status/${id}`, { status: status })
          .then(response => {
            console.log(response.data.message);
            this.fetchCandidates();  // Refresh the list after updating status
          })
          .catch(error => {
            console.log("Error updating status:", error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  /* General Container Styling */
  .container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
  }
  
  /* Header Styling */
  header {
    text-align: center;
    margin-bottom: 30px;
  }
  
  h1 {
    color: #2c3e50;
    margin-bottom: 5px;
  }
  
  p {
    color: #7f8c8d;
    font-size: 16px;
  }
  
  /* Table Styling */
  .table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  th {
    background-color: #3498db;
    color: white;
  }
  
  tr:hover {
    background-color: #f1f1f1;
  }
  
  /* Status Styling */
  .status-selected {
    color: green;
    font-weight: bold;
  }
  
  .status-rejected {
    color: red;
    font-weight: bold;
  }
  
  /* Button Styling */
  .btn {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    font-size: 14px;
    cursor: pointer;
    margin-right: 5px;
  }
  
  .btn-select {
    background-color: #2ecc71;
    color: white;
  }
  
  .btn-reject {
    background-color: #e74c3c;
    color: white;
  }
  
  .btn:hover {
    opacity: 0.9;
  }
  </style>
  