<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Papers</h1>
        <hr />
        <br /><br />
        <alert :message="message" v-if="showMessage"></alert>
        <b-form @submit="onSubmit" class="w-100">
          <b-form-group
            id="form-search-string-group"
            label="Search:"
            label-for="form-search-string-input"
          >
            <b-form-input
              id="form-search-input"
              type="text"
              v-model="SearchPaperForm.search_string"
              required
              placeholder="Search title, author, doi, etc."
            >
            </b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Search</b-button>
        </b-form>
        <br /><br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Journal</th>
              <th scope="col">Year</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(paper, index) in papers" :key="index">
              <td>{{ paper.title }}</td>
              <td>{{ paper.author }}</td>
              <td>{{ paper.journal }}</td>
              <td>{{ paper.year }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.book-update-modal
                    @click="getRef(paper)"
                  >
                    Details
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      papers: [],
      SearchPaperForm: {
        search_string: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getPapers() {
      const path = 'http://localhost:5000/search_paper';
      axios
        .get(path)
        .then((res) => {
          this.papers = res.data.papers;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    SearchPaper(payload) {
      const path = 'http://localhost:5000/search_paper';
      axios
        .post(path, payload)
        .then(() => {
          this.message = 'Search done.';
          this.showMessage = true;
          this.getPapers();
        })
        .catch((error) => {
          console.log(error);
          this.getPapers();
        });
    },
    getRef(paper) {
      this.message = paper.doi;
      this.showMessage = true;
    },
    initForm() {
      this.SearchPaperForm.search_string = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        search_string: this.SearchPaperForm.search_string,
      };
      this.SearchPaper(payload);
      this.initForm();
    },
  },
  created() {
    this.getPapers();
  },
};
</script>
