import 'dotenv/config';
import { DataTypes } from 'sequelize';
const fastify = require('fastify')({ logger: true });


const sequelize = new (require('sequelize').Sequelize)(`${process.env.PSQL}/${process.env.DB_NAME}`, {
    define: {
        timestamps: false
    },
    logging: (msg: string) => fastify.log.error(msg)
});

const user = sequelize.define('user', {
    uuid: { type: DataTypes.UUID, defaultValue: DataTypes.UUIDV4, primaryKey: true },
    tg_id: { type: DataTypes.BIGINT, allowNull: false },
    username: { type: DataTypes.STRING, allowNull: false },
    first_name: { type: DataTypes.STRING, allowNull: false },
    round: { type: DataTypes.INTEGER, defaultValue: 10 },
    is_admin: { type: DataTypes.BOOLEAN, defaultValue: false },
    full_access: { type: DataTypes.BOOLEAN, defaultValue: false },
    unlimited_time: { type: DataTypes.DATE }
});

const contour = sequelize.define('contour', {
    uuid: { type: DataTypes.UUID, defaultValue: DataTypes.UUIDV4, primaryKey: true },
    // user_id: { type: DataTypes.UUID },
    title: { type: DataTypes.STRING, allowNull: false },
    text: { type: DataTypes.STRING, allowNull: false },
    font_text: { type: DataTypes.STRING, allowNull: false },
    font_size: { type: DataTypes.INTEGER, allowNull: false },
    font_weight: { type: DataTypes.INTEGER, allowNull: false },
    text_color: { type: DataTypes.STRING, allowNull: false },
    border: { type: DataTypes.INTEGER, allowNull: false },
    border_color: { type: DataTypes.STRING, allowNull: false },
    opacity: { type: DataTypes.FLOAT, allowNull: false },
    angle: { type: DataTypes.INTEGER, allowNull: false }
});

user.hasOne(contour, {
    foreignKey: "user_id",
    sourceKey: "uuid"
});

const watermark = sequelize.define('watermark', {
    uuid: { type: DataTypes.UUID, defaultValue: DataTypes.UUIDV4, primaryKey: true },
    // user_id: { type: DataTypes.UUID },
    title: { type: DataTypes.STRING, allowNull: false },
    opacity: { type: DataTypes.FLOAT, allowNull: false },
    offsetX: { type: DataTypes.INTEGER, allowNull: false },
    offsetY: { type: DataTypes.INTEGER, allowNull: false }
});

user.hasOne(watermark, {
    foreignKey: "user_id",
    sourceKey: "uuid"
});

fastify.get('/', () => ({ msg: 'OK' }));

fastify.put('/new', async (req: Request & any, res: Response & any) => {
    console.log(req.body, req.headers);
    const webapp = JSON.parse(req.headers.authorization);

    try {
        const models = {
            contour,
            watermark
        };
        await models[req.body.type as keyof typeof models].create({ ...req.body, user_id: req.headers.authorization });
        res.code(200).send({ msg: 'ok' });
    } catch (e) {
        res.code(500).send(e);
        console.error(e, req.body);
    }
});

(async () => {
    try {
        await fastify.register(require('@fastify/rate-limit'), { max: 100, timeWindow: '1 minute' });
        await fastify.register(require('@fastify/cors'), { origin: '*' });
        await fastify.listen({ port: 4000, host: '0.0.0.0' });
        await sequelize.authenticate();
        await sequelize.query("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '" + process.env.DB_NAME + "' AND pid <> pg_backend_pid() AND state in ('idle');");
        console.log('saver launched');
    } catch (err) {
        fastify.log.error(err);
        process.exit(1);
    }
})();
