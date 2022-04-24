import React from "react";

//material
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

import '../../assets/styles/cardStyle.css';



export default function CardAllContent() {

  return (
    <>
          <Card sx={{ maxWidth: {xs : '100%', md: 300, xl: 500 }, width: {xs : '100%', md : 300, xl: 500} , mr: {xs: 0, md: 2, xl: 3}, ml: {xs: 0, md: 2, xl: 3}, mt: {xs: 3} }}>
            <CardMedia
              component="img"
              alt="image"
              src="https://www.creative-tim.com/learning-lab/tailwind-starter-kit/img/team-1-800x800.jpg"
              sx={{ height: 200 }}
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Fanomezantsoa
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Lizards are a widespread group of squamate reptiles, with over 6,000
                species, ranging across all continents except Antarctica
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small">Editer</Button>
              <Button size="small">Supprimer</Button>
            </CardActions>
          </Card>

          <Card sx={{ maxWidth: {xs : '100%', md: 300, xl: 500 }, width: {xs : '100%', md : 300, xl: 500} , mr: {xs: 0, md: 2, xl: 3}, ml: {xs: 0, md: 2, xl: 3}, mt: {xs: 3} }}>
            <CardMedia
              component="img"
              alt="image"
              src="https://www.creative-tim.com/learning-lab/tailwind-starter-kit/img/team-1-800x800.jpg"
              sx={{ height: 200 }}
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Dama
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Lizards are a widespread group of squamate reptiles, with over 6,000
                species, ranging across all continents except Antarctica
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small">Editer</Button>
              <Button size="small">Supprimer</Button>
            </CardActions>
          </Card>

           <Card sx={{ maxWidth: {xs : '100%', md: 300, xl: 500 }, width: {xs : '100%', md : 300, xl: 500} , mr: {xs: 0, md: 2, xl: 3}, ml: {xs: 0, md: 2, xl: 3}, mt: {xs: 3} }}>
            <CardMedia
              component="img"
              alt="image"
              src="https://www.creative-tim.com/learning-lab/tailwind-starter-kit/img/team-1-800x800.jpg"
              sx={{ height: 200 }}
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Fandresena
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Lizards are a widespread group of squamate reptiles, with over 6,000
                species, ranging across all continents except Antarctica
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small">Editer</Button>
              <Button size="small">Supprimer</Button>
            </CardActions>
          </Card>
          
          
    </>
  );
}