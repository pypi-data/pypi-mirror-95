"""Convert tmx to epub."""
import asyncio
from pathlib import Path

import logzero
from logzero import logger

from pprint import pprint
from absl import app, flags

# from tmx2epub.xml_iter import xml_iter
# from .browse_filename import browse_filename
# from .gen_filename import gen_filename

from extend_noip.get_ppbrowser import LOOP, BROWSER
from .login_noip import login_noip
from .fetch_myservices import fetch_myservices
from .fetch_lastupdate import fetch_lastupdate
from .update_service import update_service

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "username",
    "",  # use NOIP_USERNAME environ var (can be set in .env) if empty
    "noip username ot email address",
    short_name="u",
)
flags.DEFINE_string(
    "password",  # use NOIP_PASSOWRD environ var (can be set in .env) if empty
    "",  # filename dir if empty
    "noip password",
    short_name="p",
)

flags.DEFINE_boolean(
    "info", False, "print account info and exit", short_name="i",
)
flags.DEFINE_boolean(
    "debug", False, "print verbose debug messages", short_name="d",
)
flags.DEFINE_boolean("version", False, "print version and exit", short_name="V")


def proc_argv(_):  # pylint: disable=too-many-branches  # noqa: C901
    """Proc_argv in absl."""
    # version = "0.1.0"

    if FLAGS.version:
        from extend_noip import __version__

        print("extend_noip %s 20210222, brought to you by mu@qq41947782" % __version__)
        raise SystemExit(0)

    if FLAGS.debug:
        logzero.loglevel(10)  # logging.DEBUG
    else:
        logzero.loglevel(20)  # logging.INFO

    # args = dict((elm, getattr(FLAGS, elm)) for elm in FLAGS)
    logger.debug(
        "\n\t available args: %s", dict((elm, getattr(FLAGS, elm)) for elm in FLAGS)
    )

    args = ["username", "password", "info", "debug"]

    debug = FLAGS.debug
    if debug:
        logger.debug("\n\t args: %s", [[elm, getattr(FLAGS, elm)] for elm in args])

    try:
        page = LOOP.run_until_complete(login_noip(FLAGS.username, FLAGS.password,))
    except Exception as exc:
        logger.error("login: %s%", exc)
        logger.error("Unable to login it appears, exiting")
        raise SystemExit(1)

    myservices = LOOP.run_until_complete(fetch_myservices(page))
    logger.debug("my services: %s", myservices)
    _ = """ cant do this unless using different page handlers?
    coros = [
        fetch_lastupdate(link, page, ip_info=True) for link in myservices[1]
    ]
    res = LOOP.run_until_complete(asyncio.gather(*coros))
    # """

    def last_updateinfo(links):
        res = []
        # for link in myservices[1]:
        for link in links:
            try:
                coro = fetch_lastupdate(link, page, ip_info=True)
                _ = LOOP.run_until_complete(coro)
            except Exception as exc:
                logger.error("%s, exc: %s", link, exc)
                _ = str(exc)
            res.append(_)
        return res

    res = last_updateinfo(myservices[1])

    logger.debug("%s", [myservices, res])
    pprint("")
    pprint(myservices)
    pprint("")
    pprint(res)

    if FLAGS.i:
        raise SystemExit(0)

    # attempt to update all
    res_up = []
    for link in myservices[1]:
        # for link in links:
        try:
            coro = fetch_lastupdate(link, page, ip_info=True)
            _ = LOOP.run_until_complete(coro)
        except Exception as exc:
            logger.error("%s, exc: %s", link, exc)
            _ = str(exc)
        logger.debug(" **link: %s, %s", link, _)
        res_up.append(_)

    pprint("")
    pprint(res_up)

    # raise SystemExit("quit by intention...")


def main():
    """Main."""
    app.run(proc_argv)


if __name__ == "__main__":
    main()
