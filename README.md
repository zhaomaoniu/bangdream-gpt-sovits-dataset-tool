# BanGDream GPT-SoVITS Dataset Tool

这是一个用于生成 BanG Dream! GPT-SoVITS 数据集的工具。通过从 [Bestdori](https://bestdori.com/) 获取活动剧情数据和语音数据，整理生成用于训练 GPT-SoVITS 模型的数据集。

## 安装
<details open>
    <summary>pip</summary>

    pip install -r requirements.txt
</details>

<details>
    <summary>pdm</summary>

    pdm install
</details>

<details>
    <summary>poetry</summary>

    poetry install
</details>

<details>
    <summary>conda</summary>

    conda create --name bangdream-env --file requirements.txt
    conda activate bangdream-env
</details>

## 使用方法

1. 克隆此仓库：
    ```bash
    git clone https://github.com/zhaomaoniu/bangdream-gpt-sovits-dataset-tool.git
    cd bangdream-gpt-sovits-dataset-tool
    ```

2. 运行 `story_download.py` 下载活动剧情数据：
    ```bash
    python story_download.py
    ```
    下载的数据将保存在 `eventstory` 目录下。

3. 运行 `voice_download.py` 下载语音数据：
    ```bash
    python voice_download.py --cid {cid}
    ```
    `{cid}` 为你希望下载的角色的 ID，例如 `1` 代表「戸山香澄」。你可以在 [这里](https://bestdori.com/api/characters/all.2.json) 查看所有角色的 ID。

    下载的数据将保存在 `voice` 目录下。

4. 运行 `list_generator.py` 生成数据集列表：
    ```bash
    python list_generator.py --cid {cid} --cname {cname} --length {length}
    ```
    `{cid}` 为你希望生成的角色的 ID。

    `{cname}` 为你希望生成的角色的名字。

    `{length}` 为你希望生成的数据集的长度，例如 `200` 代表生成 200 条数据。

    生成的数据集列表将保存在项目根目录下。
