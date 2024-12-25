const { createApp } = Vue;

createApp({
  data() {
    return {
      fileName: "",
      fileContent: "",
      processedContent: ""
    };
  },
  methods: {
    async selectFile() {
      const result = await eel.open_file_dialog()();
      if (result.error) {
        alert(result.error);
      } else {
        this.fileName = result.file_name;

        // YAMLの内容をそのまま表示
        if (result.file_name.endsWith(".yaml")) {
          try {
            this.fileContent = jsyaml.dump(result.content);
          } catch (error) {
            alert("Error parsing YAML content!");
            console.error(error);
          }
        } else {
          this.fileContent = JSON.stringify(result.content, null, 2);
        }

        this.processedContent = ""; // ファイル選択時に初期化
      }
    },
    async processContent() {
      if (this.fileContent && this.fileName) {
        const result = await eel.process_file_content(this.fileName, this.fileContent)();
        this.processedContent = result; // Pythonからの結果を表示
      } else {
        alert("No content or file name to process!");
      }
    },
    async saveFile() {
      if (!this.fileName) {
        alert("No file selected!");
        return;
      }

      const newExtension = this.fileName.endsWith(".json") ? ".yaml" : ".json";
      const newFileName = this.fileName.replace(/\.(json|yaml)$/, newExtension);

      const savePath = await eel.save_file_dialog(newFileName)(); // Python側で保存先を取得
      if (savePath) {
        const contentToSave = newExtension === ".yaml"
          ? jsyaml.dump(JSON.parse(this.processedContent))
          : JSON.stringify(jsyaml.load(this.processedContent), null, 2);

        await eel.save_file(savePath, contentToSave)();
        alert(`File saved as: ${savePath}`);
      }
    }
  }
}).mount("#app");
