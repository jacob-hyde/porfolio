export interface Profile {
  id: number;
  name: string;
  title: string;
  bio: string;
  skills: Skill[];
}

export interface Project {
  id: number;
  title: string;
  description: string;
  image_url: string;
  github_url: string;
  live_url: string | null;
  tech_stack: string[];
  created_at: string | null;
}

export interface Skill {
  id: number;
  name: string;
  category: string;
  proficiency: number;
}

export interface PortfolioState {
  profile: Profile | null;
  projects: Project[];
  skills: Skill[];
  loading: boolean;
  error: string | null;
}
