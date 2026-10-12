# BrickWorld Engine – Stone Age Greybox v0.1

Creates a non-playable Blender scene and 16:9 preview. Blender Python is required; ordinary Android Python/Pydroid cannot import `bpy` without a compatible Blender runtime.

## Run with GitHub Actions (Android browser)

1. Create a GitHub repository `BrickWorld-Engine`.
2. Upload `BrickWorld_Prototype_01.py` to the repository root.
3. Add `.github/workflows/build-blender.yml` at the **exact** path, using GitHub's **Add file → Create new file** feature (GitHub creates the folders).
4. Commit changes to the default branch.
5. Go to **Actions → Build BrickWorld Blender Scene → Run workflow**.
6. Wait for the build. Open its run details and download the **BrickWorld-Prototype-01** artifact ZIP.
7. Extract ZIP on Android to get `.blend` and `.png`. View `.png` in Gallery. The `.blend` file requires Blender or another compatible 3D application to inspect; GitHub doesn't convert or display it natively.

GitHub Actions availability, billing, and runtime packages depend on account/repository settings. A render may fail on cloud runners; inspect logs if that happens.

## Run on a computer with Blender

`blender -b --python BrickWorld_Prototype_01.py -- --output ./output`

**Warning:** The script clears the active Blender scene before generating its objects.
