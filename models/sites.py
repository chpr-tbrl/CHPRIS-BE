import logging
logger = logging.getLogger(__name__)

from Configs import baseConfig
config = baseConfig()

from peewee import DatabaseError
from peewee import IntegrityError

from schemas.sites.sites import Sites
from schemas.sites.regions import Regions
from schemas.users.users import Users
from schemas.users.users_sites import Users_sites

from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import Unauthorized

class Site_Model:
    """
    """
    def __init__(self) -> None:
        """
        """
        self.Sites = Sites
        self.Regions = Regions
        self.Users = Users
        self.Users_sites = Users_sites

    def create_region(self, name: str, region_code: str) -> str:
        """
        Add region to database.

        Arguments:
            name: str

        Returns:
            str
        """
        try:
            try:
                self.Regions.get(self.Regions.name == name)
            except self.Regions.DoesNotExist:
                logger.debug("creating region '%s' ..." % name)

                region = self.Regions.create(name=name, region_code=region_code)

                logger.info("- Region '%s' successfully created" % name)
                return str(region)
            else:
                logger.error("Region '%s' exist" % name)
                raise Conflict()
        
        except DatabaseError as err:
            logger.error("creating region '%s' failed check logs" % name)
            raise InternalServerError(err) from None

    def update_region(self, region_id:int, name: str, region_code: str) -> int:
        """
        Update region.

        Arguments:
            region_id: int,
            name: str

        Returns:
            int
        """
        try:
            region = self.Regions.update(
                name = name,
                region_code=region_code
            ).where(
                self.Regions.id == region_id
            )

            region.execute()

            return region_id
        
        except DatabaseError as err:
            logger.error("updating region '%s' failed check logs" % name)
            raise InternalServerError(err) from None

    def fetch_region(self, region_id: str) -> dict:
        """
        Fetch a single region.

        Arguments:
            region_id: str
        
        Returns:
            dict
        """
        try:
            logger.debug("finding region %s ..." % region_id)
            
            result = []
            
            regions = (
                self.Regions.select()
                .where(self.Regions.id == region_id)
                .dicts()
            )

            for region in regions.iterator():
                result.append(region)

            # check for duplicates
            if len(result) > 1:
                logger.error("Multiple regions %s found" % region_id)
                raise Conflict()

            # check for no user
            if len(result) < 1:
                logger.error("No region found")
                raise Unauthorized()

            logger.info("- Region %s found" % region_id)

            return result[0]

        except DatabaseError as err:
            logger.error("failed to find region %s check logs" % region_id)
            raise InternalServerError(err) from None

    def fetch_regions(self) -> list:
        """
        Fetch all regions.

        Arguments:
            None

        Returns:
            list
        """
        try:
            logger.debug("fetching all region records ...")

            result = []
            
            regions = (
                self.Regions.select()
                .dicts()
            )
            for region in regions.iterator():
                result.append(region)

            logger.info("- Successfully fetched all regions")
            
            return result

        except DatabaseError as err:
            logger.error("failed to fetch all regions check logs")
            raise InternalServerError(err) from None

    def create_site(self, name: str, region_id: int, site_code: str) -> str:
        """
        Add site to database.

        Arguments:
            name: str,
            region_id: int,
            site_code: str

        Returns:
            str
        """
        try:
            try:
                self.Sites.get(self.Sites.name == name, self.Sites.region_id == region_id)
            except self.Sites.DoesNotExist:
                logger.debug("creating site '%s' ..." % name)

                site = self.Sites.create(name=name, region_id=region_id, site_code=site_code)

                logger.info("- Site '%s' successfully created" % name)

                user_sites = []
                user_sites.append(site.id)

                super_admin = config["SUPER_ADMIN"]

                try:
                    user = self.Users.get(self.Users.email == super_admin["EMAIL"])
                except self.Users.DoesNotExist:
                    logger.error("No user found")
                    raise Unauthorized()
                else:
                    logger.info("- Adding super admin to site: %s" % name)

                    for site_id in user_sites:
                        try:
                            self.Users_sites.create(user_id=user.id, site_id=site_id)
                            logger.info("- Successfully added site_id=%s to user_id=%s" % (site_id, user.id))
                        except IntegrityError as error:
                            logger.error(error)
                    
                return str(site)
            else:
                logger.error("Site '%s' with region_id=%s exist or site_code '%s' with region_id=%s exist" % (name, region_id, site_code, region_id))
                raise Conflict()

        except DatabaseError as err:
            logger.error("creating site '%s' failed check logs" % name)
            raise InternalServerError(err) from None

    def update_site(self, site_id: int, name: str, site_code: str) -> str:
        """
        Update site.

        Arguments:
            site_id: int,
            name: str,
            site_code: str

        Returns:
            str
        """
        try:
            site = self.Sites.update(
                name=name,
                site_code=site_code
            ).where(
                self.Sites.id == site_id
            )

            site.execute()

            return site_id

        except DatabaseError as err:
            logger.error("updating site '%s' failed check logs" % name)
            raise InternalServerError(err) from None

    def fetch_site(self, site_id: str = None) -> dict:
        """
        Fetch a single site.

        Arguments:
            site_id: str
        
        Returns:
            dict
        """
        try:
            logger.debug("finding site %s ..." % site_id)
            
            result = []

            sites = (
                self.Sites.select()
                .where(self.Sites.id == site_id)
                .dicts()
            )

            for site in sites.iterator():
                result.append(site)

            # check for duplicates
            if len(result) > 1:
                logger.error("Multiple sites %s found" % site_id)
                raise Conflict()

            # check for no user
            if len(result) < 1:
                logger.error("No site found")
                raise Unauthorized()

            logger.info("- Site %s found" % site_id)

            return result[0]

        except DatabaseError as err:
            logger.error("failed to find site %s check logs" % site_id)
            raise InternalServerError(err) from None

    def fetch_sites(self, region_id: int) -> dict:
        """
        Fetch all sites for a region.

        Arguments:
            region_id: int

        Returns:
            list
        """
        try:
            logger.debug("fetching all site records ...")

            result = []
            
            sites = (
                self.Sites.select().where(self.Sites.region_id == region_id)
                .dicts()
            )

            for site in sites.iterator():
                result.append(site)

            logger.info("- Successfully fetched all sites")

            return result

        except DatabaseError as err:
            logger.error("failed to fetch all sites check logs")
            raise InternalServerError(err) from None
