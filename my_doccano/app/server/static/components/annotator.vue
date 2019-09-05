<template lang="pug">
  div(@click="setSelectedRange")
    div.changeBtn
      span 全局匹配
      a.button.tooltip.is-tooltip-bottom(
        v-on:click="changeCheckAll"
        v-bind:data-tooltip="[checkAll ? checkAllTrue : checkAllFalse]"
      )
        span.icon
          i.far(v-bind:class="[checkAll ? 'fa-check-circle' : 'fa-circle']")
    div.column.is-1.has-text-right
    span.text-sequence(
      v-for="r in chunksWithLabel"
      v-bind:class="getChunkClass(r)"
      v-bind:data-tooltip="id2label[r.label].text"
      v-bind:style="{ \
        backgroundColor: id2label[r.label].background_color, \
        color: id2label[r.label].text_color \
      }"
      class="r.label"
    )
      span
        span(
          v-for="highlightedChunk in getSearchHighlightedChunks(textPart(r))"
          v-bind:class="highlightedChunk.highlight && 'has-background-warning'"
        ) {{ highlightedChunk.content }}
      button.delete.is-small(v-if="id2label[r.label].text_color", v-on:click="removeLabel(r)")
      
      //- button.delete.is-small(style="width:45px;height:25px;")
</template>

<script>
export default {
  props: {
    labels: {
      type: Array, // [{id: Integer, color: String, text: String}]
      default: () => [],
    },
    searchQuery: {
      type: String,
      default: '',
    },
    text: {
      type: String,
      default: '',
    },
    entityPositions: {
      type: Array, // [{'startOffset': 10, 'endOffset': 15, 'label_id': 1}]
      default: () => [],
    },
  },

  data: () => ({
    startOffset: 0,
    endOffset: 0,
    selectText:"",
    checkAll:false,
    checkAllTrue:"单击关闭全局匹配模式",
    checkAllFalse:"单击开启全局匹配模式"
  }),

  computed: {
    sortedEntityPositions() {
      /* eslint-disable vue/no-side-effects-in-computed-properties */
      this.entityPositions = this.entityPositions.sort((a, b) => a.start_offset - b.start_offset);
      return this.entityPositions;
      
      /* eslint-enable vue/no-side-effects-in-computed-properties */
    },

    chunks() {
      const res = [];
      let left = 0;
      const range = this.selectText;
      for (let i = 0; i < this.sortedEntityPositions.length; i++) {
        const e = this.sortedEntityPositions[i];
        const l = this.makeLabel(left, e.start_offset);
        res.push(l);
        res.push(e);
        left = e.end_offset;
      }
      const l = this.makeLabel(left, this.text.length);
      res.push(l);
      return res;
    },
    chunksWithLabel() {
      return this.chunks.filter(r => this.id2label[r.label]);
      
    },

    id2label() {
      const id2label = {};
      // default value;
      id2label[-1] = {
        text_color: '',
        background_color: '',
      };
      for (let i = 0; i < this.labels.length; i++) {
        const label = this.labels[i];
        id2label[label.id] = label;
      }
      return id2label;
    },
  },

  watch: {
    entityPositions() {
      this.resetRange();
    },
  },
  mounted() {
    console.log('$props',this.$props);
  },
  methods: {
    changeCheckAll(){
      this.checkAll = !this.checkAll
    },
    getSearchHighlightedChunks(text) {
      if (this.searchQuery) {
        const chunks = [];
        let currentText = text;
        let nextIndex;

        do {
          nextIndex = currentText.toLowerCase().indexOf(this.searchQuery.toLowerCase());

          if (nextIndex !== -1) {
            chunks.push({
              content: currentText.substring(0, nextIndex),
              highlight: false,
            });
            chunks.push({
              content: currentText.substring(nextIndex, nextIndex + this.searchQuery.length),
              highlight: true,
            });
            nextIndex += this.searchQuery.length;
            currentText = currentText.substring(nextIndex);
          } else {
            chunks.push({
              content: currentText.substring(nextIndex),
              highlight: false,
            });
          }
        } while (nextIndex !== -1);
        return chunks.filter(({ content }) => content);
      }
      return [{ content: text, highlight: false }];
    },

    getChunkClass(chunk) {
      if (!chunk.id) {
        return {};
      }

      const label = this.id2label[chunk.label];
      return [
        'tooltip is-tooltip-bottom',
        { tag: label.text_color },
      ];
    },

    setSelectedRange() {
      let start;
      let end;
      if (window.getSelection) {
        let range = window.getSelection().getRangeAt(0);
        const preSelectionRange = range.cloneRange();
        preSelectionRange.selectNodeContents(this.$el);
        preSelectionRange.setEnd(range.startContainer, range.startOffset);
        start = [...preSelectionRange.toString()].length-4;
        end = start + [...range.toString()].length;

        this.selectText=range.toString()
      } else if (document.selection && document.selection.type !== 'Control') {
        const selectedTextRange = document.selection.createRange();
        const preSelectionTextRange = document.body.createTextRange();
        preSelectionTextRange.moveToElementText(this.$el);
        preSelectionTextRange.setEndPoint('EndToStart', selectedTextRange);
        start = [...preSelectionTextRange.text].length-4;
        end = start + [...selectedTextRange.text].length;
        
      
      }
      this.startOffset = start;
      this.endOffset = end;
      console.log(this.startOffset, end,"*****"); // eslint-disable-line no-console
    },

    validRange() {
      if (this.startOffset === this.endOffset) {
        return false;
      }
      if (this.startOffset > this.text.length || this.endOffset > this.text.length) {
        return false;
      }
      if (this.startOffset < 0 || this.endOffset < 0) {
        return false;
      }
      for (let i = 0; i < this.entityPositions.length; i++) {
        const e = this.entityPositions[i];
        if ((e.start_offset <= this.startOffset) && (this.startOffset < e.end_offset)) {
          return false;
        }
        if ((e.start_offset < this.endOffset) && (this.endOffset < e.end_offset)) {
          return false;
        }
        if ((this.startOffset < e.start_offset) && (e.start_offset < this.endOffset)) {
          return false;
        }
        if ((this.startOffset < e.end_offset) && (e.end_offset < this.endOffset)) {
          return false;
        }
      }
      return true;
    },

    resetRange() {
      this.startOffset = 0;
      this.endOffset = 0;
    },

    textPart(r) {
      return [...this.text].slice(r.start_offset, r.end_offset).join('');
    },

    addLabel(labelId) {
      let range = window.getSelection().getRangeAt(0);
      let indexArr = []
      if (this.validRange()) {
        if(this.checkAll){
          let index = this.text.indexOf(this.selectText)
          while(index > -1){
            indexArr.push({
              start_offset: index,
              end_offset: index + this.selectText.length,
              label: labelId
            })
            index = this.text.indexOf(this.selectText,index + 1);
          }
        }else{
          indexArr = {
            start_offset: this.startOffset,
            end_offset: this.endOffset,
            label: labelId,
          }
        }
        this.$emit('add-label', indexArr);
      }
    },

    removeLabel(index) {
      this.$emit('remove-label', index);
    },

    makeLabel(startOffset, endOffset) {
      const label = {
        id: 0,
        label: -1,
        start_offset: startOffset,
        end_offset: endOffset,
      };
      return label;
    },
  },
};
</script>

<style>
.changeBtn{
  width:32%;
  position: absolute;
  font-size: 16px;
  top: -66px;
  right: 33%;
  text-align: right;
}
.changeBtn span{
  margin-right:5px;
}
.changeBtn a{
  top: 7px;
}
</style>
