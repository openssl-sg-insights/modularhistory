import ModuleUnionCard from "@/components/cards/ModuleUnionCard";
import Layout from "@/components/Layout";
import PageHeader from "@/components/PageHeader";
import { Collection } from "@/types/modules";
import ShareIcon from "@mui/icons-material/Share";
import { Box, Button, Container, useMediaQuery } from "@mui/material";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import axios from "axios";
import { GetStaticPaths, GetStaticProps } from "next";
import { NextSeo } from "next-seo";
import Link from "next/link";
import React, { FC, useState } from "react";
import {
  EmailIcon,
  EmailShareButton,
  FacebookIcon,
  FacebookShareButton,
  TwitterIcon,
  TwitterShareButton,
} from "react-share";
import { GlobalTheme } from "../_app.page";

interface CollectionProps {
  collection: Collection;
}

/**
 * The collections page:
 * http://www.modularhistory.com/collections
 */
const CollectionDetailPage: FC<CollectionProps> = ({ collection }: CollectionProps) => {
  const smallScreen = useMediaQuery<GlobalTheme>((theme) => theme.breakpoints.down("sm"));
  return (
    <Layout>
      <NextSeo
        title={collection.title}
        canonical={"/collections"}
        description={`"${collection.title}", a collection of historical occurrences, entities, sources, and more.`}
      />
      <PageHeader>{collection.title}</PageHeader>
      <Box sx={{ m: 2 }}>
        <Typography
          sx={{ fontFamily: "Segoe UI", fontWeight: 500, fontSize: 40 }}
          variant="h4"
          align="center"
        >
          {collection.title}
        </Typography>
      </Box>
      {smallScreen ? (
        <MobileSharingButtons collection={collection} />
      ) : (
        <DesktopSharingButtons collection={collection} />
      )}
      ;
      <Container>
        <Grid container spacing={2}>
          {[collection.propositions, collection.entities, collection.quotes, collection.sources]
            .flat()
            .map((module) => (
              <Grid item key={module.slug} xs={6} sm={4} md={3}>
                <Link href={module.absoluteUrl}>
                  <a>
                    <ModuleUnionCard module={module} />
                  </a>
                </Link>
              </Grid>
            ))}
        </Grid>
      </Container>
    </Layout>
  );
};
export default CollectionDetailPage;

export const getStaticProps: GetStaticProps = async ({ params }) => {
  let collection = {};
  let notFound = false;
  const { slug } = params || {};

  await axios
    .get(`http://django:8000/api/collections/${slug}/`)
    .then((response) => {
      collection = response.data;
    })
    .catch((error) => {
      if (error.response?.status === 404) {
        notFound = true;
      } else {
        throw error;
      }
    });

  return {
    props: { collection },
    notFound,
    revalidate: 10,
  };
};

export const getStaticPaths: GetStaticPaths = async () => {
  return {
    paths: [],
    fallback: "blocking",
  };
};

const MobileSharingButtons: FC<CollectionProps> = ({ collection }: CollectionProps) => {
  const [showIcons, setShowIcons] = useState(false);
  const onClick = () => {
    setShowIcons((prevState) => !prevState);
  };
  return (
    <Grid container justifyContent="flex-end">
      <Button variant="contained" color="primary" onClick={onClick} sx={{ borderRadius: "50%" }}>
        <ShareIcon />
      </Button>
      <>
        {showIcons ? (
          <Grid container justifyContent="flex-end">
            <SharingButtonGroup collection={collection} />
          </Grid>
        ) : null}
      </>
    </Grid>
  );
};

const DesktopSharingButtons: FC<CollectionProps> = ({ collection }: CollectionProps) => {
  return (
    <Grid container justifyContent="flex-end">
      <SharingButtonGroup collection={collection} />
    </Grid>
  );
};

const SharingButtonGroup: FC<CollectionProps> = ({ collection }: CollectionProps) => {
  return (
    <>
      <Grid
        container
        alignItems="center"
        justifyContent="center"
        spacing={2}
        sx={{ m: 2, maxWidth: 200 }}
      >
        <Grid item>
          <FacebookShareButton
            url={`https://modularhistory.com/collections/${collection.slug}`}
            quote={collection.title}
          >
            <FacebookIcon size={36} round={true} />
          </FacebookShareButton>
        </Grid>
        <Grid item>
          <TwitterShareButton
            url={`https://modularhistory.com/collections/${collection.slug}`}
            title={collection.title}
          >
            <TwitterIcon size={36} round={true} />
          </TwitterShareButton>
        </Grid>
        <Grid item>
          <EmailShareButton
            url={`https://modularhistory.com/collections/${collection.slug}`}
            subject={collection.title}
          >
            <EmailIcon size={36} round={true} />
          </EmailShareButton>
        </Grid>
      </Grid>
    </>
  );
};
