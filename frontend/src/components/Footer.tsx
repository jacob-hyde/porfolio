import React from 'react';
import { Box, Container, IconButton } from '@mui/material';
import {
  GitHub as GitHubIcon,
  LinkedIn as LinkedInIcon,
  Email as EmailIcon,
} from '@mui/icons-material';

const Footer: React.FC = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: 'background.paper',
      }}
    >
      <Container maxWidth="lg">
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
          <IconButton
            href="https://github.com/jacobhyde"
            target="_blank"
            rel="noopener noreferrer"
            color="primary"
          >
            <GitHubIcon />
          </IconButton>
          <IconButton
            href="https://linkedin.com/in/jacobhyde"
            target="_blank"
            rel="noopener noreferrer"
            color="primary"
          >
            <LinkedInIcon />
          </IconButton>
          <IconButton
            href="mailto:jacob.hyde@example.com"
            color="primary"
          >
            <EmailIcon />
          </IconButton>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
