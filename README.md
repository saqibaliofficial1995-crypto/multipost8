# Channel 8 — YouTube Automation Pipeline (`multipost8`)

Cloud-native, 100% automated YouTube video upload, metadata optimization, comment responder, and analytics pipeline running exclusively on GitHub Actions.

## Channel Overview
- **Owner Account:** `sheryarali0611@gmail.com`
- **GitHub Account:** `saqibaliofficial1995-crypto`
- **YouTube Channel:** `Historiana`
- **Channel ID:** `UC2okK0Nex0qijQb1omY8x2Q`
- **Initial Inbox Count:** 66 videos
- **Target Cadence:** 3 uploads / day (05:00 / 11:00 / 17:00 PKT) via GitHub Actions schedule (`0 0,6,12 * * *`)
- **Execution Target:** 100% cloud-hosted on GitHub Actions (`ubuntu-latest`). User PC is completely OFF.

## Architecture & Authentication (Dual-Token Auth)
> **Special Architectural Note:**  
> This channel uses a **Dual-Token Architecture**:
> - **YouTube Token (`YT_REFRESH_TOKEN`)**: Minted from the `Historiana` Brand Account containing only the 4 YouTube scopes.
> - **Drive Token (`DRIVE_REFRESH_TOKEN`)**: Minted from the primary Google Account `sheryarali0611@gmail.com` containing the Google Drive scope.
>  
> *Reason:* Google Brand Accounts are not permitted to hold the `https://www.googleapis.com/auth/drive` scope. Splitting the tokens allows the pipeline to upload directly to the `Historiana` Brand Account while safely retrieving source videos from the owner's Google Drive inbox.

## Storage & Cloud Infrastructure
- **Google Cloud Project:** `yt-multipost-channel8`
- **Drive Inbox Folder ID:** `1lL89THSx_ocxbv_K9SypQzaQs6t1a_mk`
- **Drive Uploaded Folder ID:** `1Aq04yCnot_npXHpQGZi6rDwjmGwXvRKY`
- **OAuth Client:** `Channel 8 Desktop`

## Scheduled Workflows
1. **Daily Upload (`daily-upload.yml`)**: Scheduled at `0 0,6,12 * * *` (05:00, 11:00, 17:00 PKT).
2. **Comment Replies (`comment-replies.yml`)**: Scheduled at `0 19 * * *` (00:00 PKT).
3. **Weekly Analytics (`weekly-analytics.yml`)**: Scheduled at `0 20 * * 0` (Monday 01:00 PKT).
