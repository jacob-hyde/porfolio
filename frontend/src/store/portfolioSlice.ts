import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { Profile, Project, Skill } from '../types';
import { profileApi, projectsApi, skillsApi } from '../utils/api';

interface PortfolioState {
  profile: Profile | null;
  projects: Project[];
  skills: Skill[];
  loading: boolean;
  error: string | null;
}

const initialState: PortfolioState = {
  profile: null,
  projects: [],
  skills: [],
  loading: false,
  error: null,
};

export const fetchProfile = createAsyncThunk<Profile>(
  'portfolio/fetchProfile',
  async () => {
    const response = await profileApi.get();
    return response.data;
  }
);

export const fetchProjects = createAsyncThunk<Project[]>(
  'portfolio/fetchProjects',
  async () => {
    const response = await projectsApi.list();
    return response.data;
  }
);

export const fetchSkills = createAsyncThunk<Skill[]>(
  'portfolio/fetchSkills',
  async () => {
    const response = await skillsApi.list();
    return response.data;
  }
);

const portfolioSlice = createSlice({
  name: 'portfolio',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.profile = action.payload;
      })
      .addCase(fetchProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch profile';
      })
      .addCase(fetchProjects.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProjects.fulfilled, (state, action) => {
        state.loading = false;
        state.projects = action.payload.map((project: Project) => ({
          ...project,
          image_url: project.image_url || '',
          github_url: project.github_url || '',
          tech_stack: project.tech_stack || []
        }));
      })
      .addCase(fetchProjects.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch projects';
      })
      .addCase(fetchSkills.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSkills.fulfilled, (state, action) => {
        state.loading = false;
        state.skills = action.payload;
      })
      .addCase(fetchSkills.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch skills';
      });
  }
});

export default portfolioSlice.reducer;
