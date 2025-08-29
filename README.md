# Batch Texture Fixer by Pr0j3ctCC

**Version:** 1.0.0  
**Blender Version:** 3.0+  
**Category:** Object

## 📦 Overview

Batch Texture Fixer allows you to quickly assign and adjust image textures across multiple selected objects in Blender. It provides a clean sidebar UI to set folder paths, texture mapping (scale, offset, rotation), and apply these settings uniformly across your selection.

## ✨ Features

- Batch assigns textures from a folder to selected mesh objects.
- Automatically sets up material nodes (UV → Mapping → Image Texture → Principled BSDF → Output).
- Adjust texture scale, offset, and rotation in real time via the sidebar.
- Apply mapping settings to all selected objects at once.

## 📂 UI Location

`View3D > Sidebar > Batch Texture Fixer`

## 🧪 How to Use

1. Open the **Sidebar** in 3D View (`N` key).
2. Under the **Batch Texture Fixer** tab:
   - Set the folder containing your `.png`, `.jpg`, or `.jpeg` textures.
   - Select the objects you want to assign textures to.
   - Click **Assign Textures**.
3. Adjust mapping parameters:
   - **Scale**, **Offset**, and **Rotation**.
   - Click **Apply to All** to push mapping changes across all selected objects.

## 🛠 Installation

1. Download `Batch Texture Fixer by Pr0j3ctCC.py`.
2. In Blender, go to `Edit > Preferences > Add-ons > Install`.
3. Select the `.py` file and enable the checkbox.

## 📣 Author

**Pr0j3ctCC** – Part of a suite of workflow-enhancing Blender tools.
