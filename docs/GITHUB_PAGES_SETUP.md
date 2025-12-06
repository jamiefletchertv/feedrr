# GitHub Pages Setup Guide

## Initial Setup

### 1. Repository Settings

1. Go to your repository: https://github.com/jamiefletchertv/feedrr
2. Click on **Settings** → **Pages**
3. Under **Source**, select:
   - Source: **GitHub Actions**
   - (This allows the workflow to deploy directly)

### 2. Enable Workflow Permissions

1. Go to **Settings** → **Actions** → **General**
2. Scroll down to **Workflow permissions**
3. Select **Read and write permissions**
4. Check **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

### 3. First Deploy

After pushing the `.github/workflows/build-and-deploy.yml` file:

```bash
# Commit and push the workflow
git add .github/workflows/build-and-deploy.yml
git commit -m "Add GitHub Actions workflow for automated deployment"
git push
```

The workflow will:
1. Run on every push to `main`
2. Run every 30 minutes (scheduled)
3. Can be manually triggered from the Actions tab

### 4. Manual Trigger

To manually trigger a build:
1. Go to **Actions** tab
2. Select **Build and Deploy to GitHub Pages**
3. Click **Run workflow**
4. Select branch `main`
5. Click **Run workflow**

## Accessing Your Site

Once deployed, your site will be available at:

**https://jamiefletchertv.github.io/feedrr/**

## Custom Domain (Optional)

If you want to use a custom domain:

1. Go to **Settings** → **Pages**
2. Under **Custom domain**, enter your domain (e.g., `feedrr.yourdomain.com`)
3. Click **Save**
4. Add a CNAME record in your DNS settings pointing to `jamiefletchertv.github.io`

Update `config.yaml`:
```yaml
deployment:
  custom_domain: "feedrr.yourdomain.com"  # Optional
```

## Build Schedule

The current schedule runs every 30 minutes. To change this:

Edit `.github/workflows/build-and-deploy.yml`:
```yaml
on:
  schedule:
    - cron: '*/60 * * * *'  # Every 60 minutes (hourly)
    # - cron: '0 */2 * * *'  # Every 2 hours
    # - cron: '0 0 * * *'    # Daily at midnight
```

Cron syntax:
```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
```

## Monitoring Builds

### Check Workflow Status

1. Go to **Actions** tab
2. View recent workflow runs
3. Click on a run to see detailed logs

### Troubleshooting

**Build fails:**
- Check the Actions logs for errors
- Ensure all dependencies are in `pyproject.toml`
- Verify RSS feeds are accessible

**Site not updating:**
- Check if workflow ran successfully
- Verify Git permissions are set correctly
- Check that `site/` directory is being generated

**Database issues:**
- The database is committed to the repo (in `data/`)
- Each build updates the database incrementally
- To reset: delete `data/feedrr.db` and push

## Database Versioning Strategy

The workflow commits both `site/` and `data/` directories:

```yaml
git add site/ data/
```

**Pros:**
- Incremental updates (faster builds)
- History preserved in git
- Rollback capability

**Cons:**
- Repository size grows over time
- Binary files in git (SQLite database)

### Alternative: Rebuild from scratch

If you prefer to rebuild the database each time (stateless):

1. Remove `data/` from git add in workflow:
   ```yaml
   git add site/
   ```

2. Add to `.gitignore`:
   ```
   data/
   ```

3. Each build fetches all feeds fresh (slower but cleaner)

## Costs

GitHub Pages is free for:
- ✅ Public repositories
- ✅ Up to 1GB repository size
- ✅ 100GB/month bandwidth

GitHub Actions is free for:
- ✅ Public repositories
- ✅ 2000 minutes/month

Running every 30 minutes = ~1440 builds/month
Each build takes ~2-5 minutes
Total: ~5000-7000 minutes/month

**Recommendation:** Start with 30-minute interval, adjust based on usage.

## Security Notes

- No secrets required for basic setup
- API tokens not needed (using local LLM)
- All data is public (static site)
- No user authentication needed

## Next Steps

1. ✅ Push workflow file to repository
2. ✅ Enable GitHub Pages in repository settings
3. ✅ Configure workflow permissions
4. 🔄 Wait for first build (or trigger manually)
5. 🌐 Visit https://jamiefletchertv.github.io/feedrr/
6. 📊 Monitor via Actions tab
