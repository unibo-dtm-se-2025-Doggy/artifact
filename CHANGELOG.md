# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added root `LICENSE` file (MIT).
- Added root `CHANGELOG.md`.
- Documented backend release rules: `backend/MAJOR.MINOR.PATCH` tags trigger Fly.io deployment via `.github/workflows/backend-deploy.yml`.
- Documented that backend releases in this repository do not publish packages to PyPI.

### Changed
- Backend API routes versioned to `/api/v1/*` (`/api/v1/dog-advice`, `/api/v1/dog-from-photo`).
- Added `IDogRecognitionModel` and `IDogLLMEngine` Protocol interfaces in `backend/Core/interfaces.py`.
- Frontend HTTP logic extracted into `DogApiClient` (`web/src/integrations/dogApi.ts`); `useBreedIdentification` hook now depends on `IDogApiClient` interface.
