import React, { useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Box,
  Chip,
  Stack,
  LinearProgress,
  Paper
} from '@mui/material';
import { motion } from 'framer-motion';
import { useAppDispatch, useAppSelector } from '../hooks';
import { fetchProfile, fetchProjects, fetchSkills } from '../store/portfolioSlice';

const MotionContainer = motion(Container);
const MotionCard = motion(Card);

const Portfolio: React.FC = () => {
  const dispatch = useAppDispatch();
  const { profile, projects, skills, loading } = useAppSelector((state) => state.portfolio);

  useEffect(() => {
    loadData();
  }, [dispatch]);

  const loadData = async () => {
    try {
      await Promise.all([
        dispatch(fetchProfile()),
        dispatch(fetchProjects()),
        dispatch(fetchSkills())
      ]);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  if (loading) {
    return (
      <Box sx={{ width: '100%' }}>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <MotionContainer 
      maxWidth="lg" 
      sx={{ mt: 4, mb: 4 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {profile && (
        <Box sx={{ mb: 6 }}>
          <Typography variant="h2" gutterBottom>
            {profile.name}
          </Typography>
          <Typography variant="h5" color="text.secondary" gutterBottom>
            {profile.title}
          </Typography>
          <Typography variant="body1" paragraph>
            {profile.bio}
          </Typography>
        </Box>
      )}

      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Skills
      </Typography>
      <Grid container spacing={3} sx={{ mb: 6 }}>
        {skills.map((skill) => (
          <Grid item xs={12} sm={6} md={4} key={skill.id}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                {skill.name}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {skill.category}
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={skill.proficiency} 
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Projects
      </Typography>
      <Grid container spacing={4}>
        {projects.map((project) => (
          <Grid item key={project.id} xs={12} sm={6} md={4}>
            <MotionCard
              sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
              whileHover={{ scale: 1.03 }}
              transition={{ duration: 0.2 }}
            >
              {project.image_url && (
                <CardMedia
                  component="img"
                  height="200"
                  image={project.image_url}
                  alt={project.title}
                />
              )}
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h5" component="h2">
                  {project.title}
                </Typography>
                <Typography paragraph>
                  {project.description}
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                  {project.tech_stack?.map((tech, index) => (
                    <Chip
                      key={index}
                      label={tech}
                      size="small"
                      sx={{ mt: 1 }}
                    />
                  ))}
                </Stack>
              </CardContent>
            </MotionCard>
          </Grid>
        ))}
      </Grid>
    </MotionContainer>
  );
};

export default Portfolio;
