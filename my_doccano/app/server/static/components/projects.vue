<template lang="pug">
  div(v-cloak="")
    section.hero.project-image
      div.container
        div.columns
          div.column.is-10.is-offset-1

            h1.title.is-1.has-text-white 你好, {{ username | title }}.
            h2.subtitle.is-4.has-text-white 希望你今天过得愉快！

            p(v-if="isSuperuser")
              a.button.is-medium.is-primary(v-on:click="isActive = !isActive") 创建项目

    div.modal(v-bind:class="{ 'is-active': isActive }")
      div.modal-background
      div.modal-card
        header.modal-card-head
          p.modal-card-title 创建项目
          button.delete(aria-label="close", v-on:click="isActive = !isActive")

        section.modal-card-body
          div.field
            label.label 项目名称
            div.control
              input.input(v-model="projectName", type="text", required, placeholder="请输入项目名称")
            p.help.is-danger {{ projectNameError }}

          div.field
            label.label 项目描述
            div.control
              textarea.textarea(v-model="description", required, placeholder="请输入项目描述")
            p.help.is-danger {{ descriptionError }}

          div.field
            label.label Project Type

            div.control
              select(v-model="projectType", name="项目类型", required)
                option(value="", selected="selected") ---------
                option(value="DocumentClassification") document classification
                option(value="SequenceLabeling") sequence labeling
                option(value="Seq2seq") sequence to sequence
            p.help.is-danger {{ projectTypeError }}

          div.field
            label.checkbox
              input(
                v-model="randomizeDocumentOrder"
                name="randomize_document_order"
                type="checkbox"
                style="margin-right: 0.25em;"
                required
              )
              | 随机化每个用户的文档顺序

        footer.modal-card-foot.pt20.pb20.pr20.pl20.has-background-white-ter
          button.button.is-primary(v-on:click="create()") 创建
          button.button(v-on:click="isActive = !isActive") 取消

    div.modal(v-bind:class="{ 'is-active': isDelete }")
      div.modal-background
      div.modal-card
        header.modal-card-head
          p.modal-card-title 删除项目
          button.delete(aria-label="close", v-on:click="isDelete = !isDelete")
        section.modal-card-body 确认删除该项目 ?
        footer.modal-card-foot.pt20.pb20.pr20.pl20.has-background-white-ter
          button.button.is-danger(v-on:click="deleteProject()") 创建
          button.button(v-on:click="isDelete = !isDelete") 取消

    section.hero
      div.container
        div.columns
          div.column.is-10.is-offset-1
            div.card.events-card
              header.card-header
                p.card-header-title {{ items.length }} 项目

                div.field.card-header-icon
                  div.control
                    div.select
                      select(v-model="selected")
                        option(selected) All Project
                        option Text Classification
                        option Sequence Labeling
                        option Seq2seq

              div.card-table
                div.content
                  table.table.is-fullwidth
                    tbody
                      tr(v-for="project in selectedProjects", v-bind:key="project.id")
                        td.pl15r
                          div.thumbnail-wrapper.is-vertical
                            img.project-thumbnail(
                              v-bind:src="project.image"
                              alt="Project thumbnail"
                            )

                          div.dataset-item__main.is-vertical
                            div.dataset-item__main-title
                              div.dataset-item__main-title-link.dataset-item__link
                                a.has-text-black(v-bind:href="'/projects/' + project.id")
                                  | 项目名称

                            div.dataset-item__main-subtitle 项目描述
                            div.dataset-item__main-info
                              span.dataset-item__main-update updated
                                span {{ project.updated_at | daysAgo }}

                        td.is-vertical
                          span.tag.is-normal {{ project.project_type }}

                        td.is-vertical(v-if="isSuperuser")
                          a(v-bind:href="'/projects/' + project.id + '/docs'") 编辑

                        td.is-vertical(v-if="isSuperuser")
                          a.has-text-danger(v-on:click="setProject(project)") 删除
</template>

<script>
import { title, daysAgo } from './filter';
import { defaultHttpClient } from './http';

export default {
  filters: { title, daysAgo },

  data: () => ({
    items: [],
    isActive: false,
    isDelete: false,
    project: null,
    selected: 'All Project',
    projectName: '',
    description: '',
    projectType: '',
    descriptionError: '',
    projectTypeError: '',
    projectNameError: '',
    username: '',
    isSuperuser: false,
    randomizeDocumentOrder: false,
  }),

  computed: {
    selectedProjects() {
      return this.items.filter(item => this.selected === 'All Project' || this.matchType(item.project_type));
    },
  },

  created() {
    Promise.all([
      defaultHttpClient.get('/v1/projects'),
      defaultHttpClient.get('/v1/me'),
    ]).then(([projects, me]) => {
      this.items = projects.data;
      this.username = me.data.username;
      this.isSuperuser = me.data.is_superuser;
    });
  },

  methods: {
    deleteProject() {
      defaultHttpClient.delete(`/v1/projects/${this.project.id}`).then(() => {
        this.isDelete = false;
        const index = this.items.indexOf(this.project);
        this.items.splice(index, 1);
      });
    },

    setProject(project) {
      this.project = project;
      this.isDelete = true;
    },

    matchType(projectType) {
      if (projectType === 'DocumentClassification') {
        return this.selected === 'Text Classification';
      }
      if (projectType === 'SequenceLabeling') {
        return this.selected === 'Sequence Labeling';
      }
      if (projectType === 'Seq2seq') {
        return this.selected === 'Seq2seq';
      }
      return false;
    },

    create() {
      const payload = {
        name: this.projectName,
        description: this.description,
        project_type: this.projectType,
        randomize_document_order: this.randomizeDocumentOrder,
        guideline: '请写注释参考文本',
        resourcetype: this.resourceType(),
      };
      defaultHttpClient.post('/v1/projects', payload)
        .then((response) => {
          window.location = `/projects/${response.data.id}/docs/create`;
        })
        .catch((error) => {
          this.projectTypeError = '';
          this.projectNameError = '';
          this.descriptionError = '';
          if ('resourcetype' in error.response.data) {
            this.projectTypeError = error.response.data.resourcetype;
          }
          if ('name' in error.response.data) {
            this.projectNameError = error.response.data.name[0];
          }
          if ('description' in error.response.data) {
            this.descriptionError = error.response.data.description[0];
          }
        });
    },

    resourceType() {
      if (this.projectType === 'DocumentClassification') {
        return 'TextClassificationProject';
      }
      if (this.projectType === 'SequenceLabeling') {
        return 'SequenceLabelingProject';
      }
      if (this.projectType === 'Seq2seq') {
        return 'Seq2seqProject';
      }
      return '';
    },
  },
};
</script>
