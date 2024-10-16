<template>
  <div class="container">
    <header>
      <h1>Candidate List</h1>
      <p>Manage candidate statuses by selecting or rejecting them below.</p>
    </header>

    <!-- Filters for Passing Year and Rounds -->
    <div class="filters">
      <label for="passingYear">Filter by Passing Year:</label>
      <select v-model="passingYear" @change="fetchCandidates">
        <option value="">All</option>
        <option value="2024">2024</option>
        <option value="2025">2025</option>
      </select>

      <label for="round">Filter by Round:</label>
      <select v-model="round" @change="fetchCandidates">
        <option value="">All</option>
        <option value="level1">Level 1</option>
        <option value="level2">Level 2</option>
      </select>
    </div>

    <!-- Batch Actions for selected candidates -->
    <div class="batch-actions">
      <button class="btn btn-select-all" @click="batchUpdateStatus('selected')">Select All Selected</button>
      <button class="btn btn-reject-all" @click="batchUpdateStatus('rejected')">Reject All Selected</button>
    </div>

    <table class="table">
      <thead>
        <tr>
          <th><input type="checkbox" @click="toggleAll" v-model="allSelected" /></th> <!-- Checkbox to select all -->
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Status</th>
          <th>Passing Year</th>
          <th>Round</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="candidate in candidates" :key="candidate.id">
          <td><input type="checkbox" v-model="selectedCandidates" :value="candidate.id" /></td>
          <td>{{ candidate.id }}</td>
          <td>{{ candidate.name }}</td>
          <td>{{ candidate.email }}</td>
          <td>
            <span :class="{'status-selected': candidate.status === 'selected', 'status-rejected': candidate.status === 'rejected'}">
              {{ candidate.status }}
            </span>
          </td>
          <td>{{ candidate.year }}</td> <!-- Updated to 'year' to match backend -->
          <td>{{ candidate.round }}</td>
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
      candidates: [],
      selectedCandidates: [], // To store the list of selected candidates' IDs
      passingYear: '', // Filter option for passing year
      round: '', // Filter option for round
      allSelected: false, // To handle "Select All" checkbox
    };
  },
  created() {
    this.fetchCandidates();
  },
  methods: {
    fetchCandidates() {
      // Build query params for filters
      const params = {};
      if (this.passingYear) params.year = this.passingYear; // Changed 'passing_year' to 'year'
      if (this.round) params.round = this.round;

      axios
        .get('http://127.0.0.1:5000/candidates', { params }) // Backend Flask API with filter options
        .then((response) => {
          this.candidates = response.data.candidates;
        })
        .catch((error) => {
          console.log('Error fetching candidates:', error);
        });
    },
    updateStatus(id, status) {
      axios
        .post(`http://127.0.0.1:5000/update_status/${id}`, { status: status })
        .then((response) => {
          console.log(response.data.message);
          this.fetchCandidates(); // Refresh the list after updating status
        })
        .catch((error) => {
          console.log('Error updating status:', error);
        });
    },
    batchUpdateStatus(status) {
      // Update status for all selected candidates
      const requests = this.selectedCandidates.map((id) =>
        axios.post(`http://127.0.0.1:5000/update_status/${id}`, { status: status })
      );

      // Execute all requests in parallel
      Promise.all(requests)
        .then(() => {
          this.fetchCandidates(); // Refresh after batch update
          this.selectedCandidates = []; // Clear the selection after batch action
          this.allSelected = false; // Reset select-all checkbox
        })
        .catch((error) => {
          console.log('Error updating status in batch:', error);
        });
    },
    toggleAll() {
      // Select or deselect all candidates when "Select All" checkbox is clicked
      if (this.allSelected) {
        this.selectedCandidates = this.candidates.map((candidate) => candidate.id);
      } else {
        this.selectedCandidates = [];
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

header {
  text-align: center;
  margin-bottom: 30px;
}

.filters {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.batch-actions {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-start;
}

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

.status-selected {
  color: green;
}

.status-rejected {
  color: red;
}

.btn {
  padding: 8px 12px;
  margin-right: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-select-all {
  background-color: #2ecc71;
  color: white;
}

.btn-reject-all {
  background-color: #e74c3c;
  color: white;
}
</style>
